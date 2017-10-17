from CardGames.blackjack import Blackjack
from CardGames.hand import Hand, PlayerHand
from CardGames.announcer import BlackjackAnnouncer
from player_avatar import *
from joinable_game_class import JoinableGame


class RollbotHost:
    """ A fake host for Blackjack """

    def __init__(self):
        self.display_name = "Rollbot"
        self.gold = 10000


class BlackjackExecutor(JoinableGame):

    """
    Maps user commands to game mechanics and feedback.
    "Host" and "dealer" are used interchangeably.
    """

    def __init__(self, bot, host=None):
        super().__init__(host)
        self.blackjack = Blackjack()
        self.avatar_handler = BlackjackAvatarHandler()
        self.dealer = self.init_dealer(RollbotHost())
        self.dealer_name = self.dealer.display_name
        self.standing_players = []  # Match against the dealer's hand at the end of the game
        self.announcer = BlackjackAnnouncer(bot, self.dealer_name)
        self.max_time_left = 10 * 60  # 10 minutes

    def get_avatar(self, user) -> List[PlayerHand]:
        # Players own a list of hands: initially one hand, but can be multiple after a split
        return [PlayerHand()]

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
            await self.check_dealer_turn()

    async def check_dealer_turn(self):
        are_players_standing = self.standing_players
        if are_players_standing:
            await self.announce_dealer_turn()
        else:
            await self.announcer.no_players_left()
        await self.end_game()

    async def announce_player_turn(self):
        current_player = self.players[0]
        player_name = self.avatar_handler.get_name(current_player)
        hand = self.get_current_player_hand()
        await self.announcer.next_turn(player_name, hand)

    async def announce_dealer_turn(self):
        dealer_hand = self.avatar_handler.get_first_hand(self.dealer)
        await self.announcer.dealer_turn(dealer_hand)
        await self.dealer_hit_loop()
        await self.dealer_turn_end()

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
            await self.announcer.double_down_success(wager)
            await self.stand()
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

    async def check_initial_dealer_cards(self):
        ace_or_ten = await self.dealer_ace_or_ten()
        dealer_blackjack = await self.check_initial_dealer_blackjack()
        if ace_or_ten and dealer_blackjack:
            await self.end_game()
        else:
            await self.next_turn()

    async def dealer_ace_or_ten(self) -> bool:
        hand = self.get_dealer_hand()
        first_card = hand.get_first_card()
        is_ace = self.blackjack.is_ace(first_card)
        is_ten = self.blackjack.is_ten_value(first_card)
        if is_ace or is_ten:
            await self.announcer.ace_or_ten_message(hand)
            return True

    async def check_initial_dealer_blackjack(self) -> bool:
        hand = self.get_dealer_hand()
        is_blackjack = await self.check_blackjack(hand)
        if is_blackjack:
            return True

    async def dealer_turn_end(self):
        hand = self.get_dealer_hand()
        is_blackjack = await self.check_blackjack(hand)
        is_bust = await self.check_dealer_bust()
        if not is_blackjack and not is_bust:
            await self.announcer.dealer_stand()

    async def check_dealer_bust(self):
        hand = self.get_dealer_hand()
        if hand.is_bust():
            await self.announcer.declare_dealer_bust()
            return True

    async def dealer_hit_loop(self):
        dealer_hand = self.get_dealer_hand()
        while dealer_hand.get_value() < 17:
            card = self.blackjack.hit(dealer_hand)
            await self.announcer.dealer_hit(card)

    def get_dealer_hand_value(self):
        hand = self.get_dealer_hand()
        if hand.is_bust():
            hand.set_value(0)
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
            await self.check_outcome(hand)

    async def check_blackjack(self, hand):
        if self.blackjack.is_blackjack(hand):
            await self.announcer.announce_blackjack()
            return True

    async def check_outcome(self, player_hand: PlayerHand) -> None:
        is_blackjack_win = self.is_blackjack_win(player_hand)
        is_winner = await self.is_winner(player_hand)
        is_standoff = self.is_stand_off(player_hand)
        if is_blackjack_win:
            await self.resolve_blackjack_win(player_hand)
        elif is_winner:
            await self.resolve_normal_win(player_hand)
        elif is_standoff:
            await self.resolve_standoff(player_hand)
        else:
            await self.resolve_loss(player_hand)

    async def resolve_blackjack_win(self, player_hand: PlayerHand):
        player_hand.blackjack_win()
        winnings = player_hand.get_winnings()
        self.announcer.announce_player_blackjack(winnings)

    async def resolve_normal_win(self, player_hand: PlayerHand):
        player_hand.normal_win()
        winnings = player_hand.get_winnings()
        self.announcer.win(winnings)

    async def resolve_standoff(self, player_hand: PlayerHand):
        wager = player_hand.get_wager()
        await self.announcer.stand_off(wager)

    async def resolve_loss(self, player_hand: PlayerHand):
        player_hand.lose()
        wager = player_hand.get_wager()
        await self.announcer.loss(wager)

    def is_blackjack_win(self, player_hand) -> bool:
        # Player wins if their hand is blackjack while the dealer's is not.
        host_hand = self.get_dealer_hand()
        is_host_blackjack = self.blackjack.is_blackjack(host_hand)
        is_player_blackjack = self.blackjack.is_blackjack(player_hand)
        return is_player_blackjack and not is_host_blackjack

    def is_stand_off(self, player_hand: Hand) -> bool:
        dealer_value = self.get_dealer_hand_value()
        player_value = player_hand.get_value()
        return dealer_value == player_value

    async def is_winner(self, player_hand: Hand) -> bool:
        dealer_busted = self.get_dealer_hand().is_bust()
        dealer_value = self.get_dealer_hand_value()
        hand_value = player_hand.get_value()
        player_busted = await self.check_bust(player_hand)
        if dealer_busted:
            return True
        elif player_busted:
            return False
        else:
            return hand_value > dealer_value

    async def check_bust(self, hand) -> bool:
        if hand.is_bust():
            await self.announcer.declare_player_bust()
            return True
