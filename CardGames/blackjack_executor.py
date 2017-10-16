from CardGames.blackjack import Blackjack
from typing import List
from CardGames.hand import Hand, PlayerHand
from CardGames.announcer import BlackjackAnnouncer
from player_avatar import *


class RollbotHost:
    """ A fake host for Blackjack """

    def __init__(self):
        self.display_name = "Rollbot"
        self.gold = 10000


class BlackjackExecutor:

    """
    Maps user commands to game mechanics and feedback.
    "Host" and "dealer" are used interchangeably.
    """

    def __init__(self, bot, host=None):
        self.blackjack = Blackjack()
        self.avatar_handler = BlackjackAvatarHandler()
        self.registrants = []  # Every user who has joined the game
        self.dealer = self.init_dealer(RollbotHost())
        self.dealer_name = self.dealer.display_name
        self.host = host
        self.players = []  # The turn goes to the person at the start of the list.
        self.standing_players = []  # Match against the dealer's hand at the end of the game
        self.announcer = BlackjackAnnouncer(bot, self.dealer_name)
        self.in_progress = False
        self.max_time_left = 10 * 60  # 10 minutes

    def add_user(self, user):
        # Players own a list of hands: initially one hand, but can be multiple after a split
        player = self.avatar_handler.create_avatar(user, hand=PlayerHand())
        self.players.append(player)
        self.registrants.append(user)

    async def start_game(self):
        self.dispense_cards()
        await self.show_player_cards()
        await self.show_dealer_face_up()
        await self.check_initial_dealer_cards()

    async def show_player_cards(self):

        async def announce_cards(player):
            player_name = self.avatar_handler.get_name(player)
            hand = self.avatar_handler.get_first_hand(player)
            await self.announcer.player_cards(player_name, hand)

        [await announce_cards(player) for player in self.players]

    async def show_dealer_face_up(self):
        dealer_hand = self.get_dealer_hand()
        first_card = dealer_hand.get_first_card()
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
        dealer_hand = self.avatar_handler.get_first_hand(self.dealer)
        await self.announcer.dealer_turn(dealer_hand)
        await self.dealer_hit_loop()
        await self.check_dealer_game_end()

    async def hit(self) -> None:
        hand = self.get_current_player_hand()
        new_card = self.blackjack.hit(hand)
        await self.announcer.report_hit(hand, new_card)
        await self.check_hit_bust()

    async def stand(self):
        hand = self.get_current_player_hand()
        hand.end_turn()
        await self.announcer.progressing()
        await self.check_next_hand()

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

    async def check_next_hand(self) -> None:
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
                self.blackjack.deal_card(starting_hand)

        [add_initial_cards(player) for player in self.players]
        add_initial_cards(self.dealer)

    def get_current_player(self):
        return self.players[0]

    def get_current_player_hands(self) -> List[PlayerHand]:
        current_player = self.get_current_player()
        hands = self.avatar_handler.get_hands(current_player)
        return hands

    def get_current_player_hand(self) -> PlayerHand:
        hands = self.get_current_player_hands()
        return self._get_active_hand(hands)

    async def check_hit_bust(self) -> None:
        hand = self.get_current_player_hand()
        if hand.is_bust():
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
            await self.check_next_hand()

    def knock_out_current_player(self) -> None:
        del self.players[0]

    @staticmethod
    def _get_active_hand(hands: List[PlayerHand]) -> PlayerHand:
        for hand in hands:
            if hand.is_active:
                return hand

    def init_dealer(self, host) -> PlayerAvatar:
        if host is not None:
            self.registrants.append(host)
            return self.avatar_handler.create_avatar(host, Hand())

    async def dealer_ace_or_ten(self) -> None:
        hand = self.get_dealer_hand()
        first_card = hand.get_first_card()
        is_ace_or_ten = self.blackjack.is_ten_value(first_card) or self.blackjack.is_ace(first_card)
        if is_ace_or_ten:
            await self.announcer.ace_or_ten_message(hand)

    async def check_initial_dealer_cards(self):
        """ If the dealer's visible card is a ten or ace, the dealer goes first. """
        if await self.dealer_ace_or_ten():
            await self.dealer_hit_loop()
            await self.check_dealer_game_end()
        else:
            await self.next_turn()

    async def check_dealer_game_end(self):
        hand = self.get_dealer_hand()
        is_blackjack = await self.check_blackjack(hand)
        is_bust = await self.check_dealer_bust()
        are_player_turns_remaining = self.players
        if is_blackjack or is_bust:
            await self.end_game()
        elif are_player_turns_remaining:
            await self.announcer.dealer_stand()
            await self.next_turn()
        else:
            await self.announcer.dealer_stand()
            await self.end_game()

    async def check_dealer_bust(self):
        hand = self.get_dealer_hand()
        if hand.is_bust():
            await self.announcer.declare_dealer_bust()
            return True

    async def dealer_hit_loop(self):
        hand = self.get_dealer_hand()
        hand_value = hand.get_value()
        while hand_value < 17:
            card = self.blackjack.hit(hand)
            card_value = self.blackjack.get_value(card)
            hand_value += card_value
            await self.announcer.dealer_hit(card)

    def get_host_hand_value(self):
        hand = self.get_dealer_hand()
        if hand.is_bust():
            hand.update_value(0)
        return hand.get_value()

    def get_dealer_hand(self) -> Hand:
        return self.avatar_handler.get_first_hand(self.dealer)

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
        is_winner = await self.is_winner(player_hand)
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
        elif winnings < 0:
            await self.announcer.loss(wager)

    def is_stand_off(self, player_hand: Hand) -> bool:
        host_hand = self.get_dealer_hand()
        host_value = self.get_host_hand_value()
        player_value = player_hand.get_value()
        is_host_blackjack = self.blackjack.is_blackjack(host_hand)
        is_player_blackjack = self.blackjack.is_blackjack(player_hand)
        return (is_host_blackjack == is_player_blackjack) and (host_value == player_value)

    async def is_winner(self, player_hand: Hand) -> bool:
        host_value = self.get_host_hand_value()
        hand_value = player_hand.get_value()
        host_busted = host_value <= 0
        player_busted = await self.check_bust(player_hand)
        if host_busted:
            return True
        elif player_busted:
            return False
        else:
            return hand_value > host_value

    async def check_bust(self, hand):
        if hand.is_bust():
            await self.announcer.declare_player_bust()
            return True
