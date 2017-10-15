from CardGames.blackjack import Blackjack
from typing import List
from CardGames.hand import Hand, PlayerHand
from CardGames.announcer import BlackjackAnnouncer
from player_avatar import *


class BlackjackExecutor:

    """
    Maps user commands to game mechanics and feedback.
    "Host" and "dealer" are used interchangeably.
    """

    def __init__(self, bot, host=None):
        self.blackjack = Blackjack()
        self.avatar_handler = BlackjackAvatarHandler()
        self.host = self.init_dealer(host)
        self.players = [] # The turn goes to the person at the start of the list.
        self.standing_players = []  # Match against the dealer's hand at the end of the game
        self.announcer = BlackjackAnnouncer(bot, self)
        self.in_progress = False

    def add_user(self, user):
        # Players own a list of hands: initially one hand, but can be multiple after a split
        player = self.avatar_handler.create_avatar(user, hand=PlayerHand())
        self.players.append(player)

    async def start_game(self):
        self.dispense_cards()
        await self.show_player_cards()
        await self.show_dealer_face_up()
        await self.check_dealer_cards()

    async def show_player_cards(self):

        async def announce_cards(player):
            player_name = self.avatar_handler.get_name(player)
            hand = self.avatar_handler.get_first_hand(player)
            await self.announcer.player_cards(player_name, hand)

        [await announce_cards(player) for player in self.players]

    async def show_dealer_face_up(self):
        dealer_hand = self.avatar_handler.get_hands(self.host)
        first_card = dealer_hand[0].cards[0]
        await self.announcer.dealer_card(first_card)

    async def next_turn(self):
        are_player_turns_remaining = self.players
        if are_player_turns_remaining:
            await self.announce_player_turn()
        else:
            await self.announce_dealer_turn()

    async def announce_player_turn(self):
        current_player = self.players[0]
        player_name = self.avatar_handler.get_name(current_player)
        hand = self.get_current_player_hand()
        await self.announcer.next_turn(player_name, hand)

    async def announce_dealer_turn(self):
        dealer = self.host
        dealer_hand = self.avatar_handler.get_first_hand(dealer)
        await self.announcer.dealer_turn(dealer_hand)
        await self.host_hit_loop()

    async def stand(self):
        hand = self.get_current_player_hand()
        hand.stand()
        await self.announcer.progressing()
        await self.check_next_turn()

    async def hit(self) -> None:
        hand = self.get_current_player_hand()
        new_card = self.blackjack.hit(hand)
        await self.announcer.report_hit(hand, new_card)
        await self.check_bust()

    async def attempt_double_down(self) -> None:
        hand = self.get_current_player_hand()
        if self.blackjack.double_down(hand):
            wager = hand.get_wager()
            await self.stand()
            await self.announcer.double_down_success(wager)
        else:
            await self.announcer.double_down_fail()

    async def attempt_split(self) -> None:
        hand_container = self.get_current_player_hands()
        hand = self.get_current_player_hand()
        if self.blackjack.split(hand_container, hand):
            await self.announcer.split_successful(hand)
        else:
            await self.announcer.split_fail()

    async def check_next_turn(self) -> None:
        active_hand = self.get_current_player_hand()
        if active_hand:
            await self.announcer.next_hand_options(active_hand)
        else:
            self.current_player_stand()
            await self.next_turn()

    def current_player_stand(self) -> None:
        player = self.players.pop(0)
        self.standing_players.append(player)

    def dispense_cards(self) -> None:

        def add_initial_cards(player: PlayerAvatar):
            starting_hand = self.avatar_handler.get_first_hand(player)
            num_cards = 2
            for i in range(num_cards):
                drawn_card = self.blackjack.draw_card()
                starting_hand.add_card(drawn_card)

        [add_initial_cards(player) for player in self.players]
        add_initial_cards(self.host)

    def get_current_player_hands(self) -> List[PlayerHand]:
        current_player = self.players[0]
        hands = self.avatar_handler.get_hands(current_player)
        return hands

    def get_current_player_hand(self) -> PlayerHand:
        hands = self.get_current_player_hands()
        return self._get_active_hand(hands)

    async def check_bust(self) -> None:
        hand = self.get_current_player_hand()
        if self.blackjack.is_bust(hand):
            await self.announcer.declare_player_bust()
            await self.bust_hand()
        else:
            await self.announcer.ask_hit_again()

    async def bust_hand(self) -> None:
        player_hands = self.get_current_player_hands()
        hand_to_bust = self.get_current_player_hand()
        player_hands.remove(hand_to_bust)
        await self.check_knock_out()

    async def check_knock_out(self):
        current_player_has_hand = self.get_current_player_hands()
        if not current_player_has_hand:
            self.knock_out_current_player()
            await self.next_turn()
        else:
            await self.check_next_turn()

    def knock_out_current_player(self) -> None:
        del self.players[0]

    @staticmethod
    def _get_active_hand(hands: List[PlayerHand]) -> PlayerHand:
        for hand in hands:
            if hand.is_active:
                return hand

    def init_dealer(self, host) -> PlayerAvatar:
        if host is not None:
            return self.avatar_handler.create_avatar(host, hand=Hand())

    async def dealer_ace_or_ten(self) -> None:
        hand = self.get_host_hand()
        first_card = hand.get_first_card()
        is_ace_or_ten = self.blackjack.is_ten_value(first_card) or self.blackjack.is_ace(first_card)
        if is_ace_or_ten:
            await self.announcer.ace_or_ten_message(hand)

    async def check_dealer_cards(self):
        if await self.dealer_ace_or_ten():
            await self.host_hit_loop()
            await self.check_dealer_game_end()

    async def check_dealer_game_end(self):
        hand = self.get_host_hand()
        is_blackjack = await self.check_blackjack(hand)
        is_bust = self.blackjack.is_bust(hand)
        if is_blackjack or is_bust:
            self.end_game()

    async def host_hit_loop(self):
        hand = self.get_host_hand()
        hand_value = self.get_host_hand_value()
        while hand_value < 17:
            card = self.blackjack.hit(hand)
            await self.announcer.dealer_hit(card)

    def get_host_hand_value(self):
        hand = self.get_host_hand()
        return self.blackjack.get_hand_value(hand)

    def get_host_hand(self) -> Hand:
        return self.avatar_handler.get_first_hand(self.host)

    async def end_game(self):
        """ Checks self.players in case the dealer has gotten a blackjack. """
        [await self.resolve_outcomes(player) for player in self.standing_players]
        [await self.resolve_outcomes(player) for player in self.players]
        self.in_progress = False

    async def resolve_outcomes(self, player):
        player_name = self.avatar_handler.get_name(player)
        hands = self.avatar_handler.get_hands(player)
        for hand in hands:
            await self.announcer.player_hand(player_name, hand)
            await self.check_stand_off(hand)
            await self.check_winner(hand)
            await self.announce_payout(hand)

    async def check_blackjack(self, hand):
        if self.blackjack.is_blackjack(hand):
            await self.announcer.announce_blackjack()
            return True

    async def check_stand_off(self, player_hand: PlayerHand):
        if self.is_stand_off(player_hand):
            wager = player_hand.get_wager()
            await self.announcer.stand_off(wager)

    async def check_winner(self, player_hand: PlayerHand) -> None:
        is_blackjack = await self.check_blackjack(player_hand)
        is_winner = self.is_winner(player_hand)
        if is_blackjack and is_winner:
            player_hand.blackjack_win()
        elif is_winner:
            player_hand.normal_win()
        else:
            player_hand.lose()

    async def announce_payout(self, player_hand: PlayerHand) -> None:
        winnings = player_hand.get_winnings()
        wager = player_hand.get_wager()
        if winnings > 0:
            await self.announcer.win(winnings)
        else:
            await self.announcer.loss(wager)

    def is_stand_off(self, player_hand: Hand) -> bool:
        host_hand = self.get_host_hand()
        host_value = self.get_host_hand_value()
        player_value = self.blackjack.get_hand_value(player_hand)
        is_host_blackjack = self.blackjack.is_blackjack(host_hand)
        is_player_blackjack = self.blackjack.is_blackjack(player_hand)
        return (is_host_blackjack == is_player_blackjack) and (host_value == player_value)

    def is_winner(self, player_hand: Hand) -> bool:
        host_value = self.get_host_hand_value()
        player_value = self.blackjack.get_hand_value(player_hand)
        return player_value > host_value
