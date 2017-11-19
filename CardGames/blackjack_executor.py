from player_avatar import *

from CardGames.announcer import BlackjackAnnouncer
from CardGames.blackjack import Blackjack
from CardGames.dealer import BlackjackDealer
from CardGames.hand import Hand, PlayerHand
from CardGames.result_checker import BlackjackResultChecker
from Core.core_game_class import JoinableGame


class RollbotHost:
    """ A fake host for Blackjack """

    def __init__(self):
        self.display_name = "Rollbot"
        self.gold = 10000


class BlackjackExecutor(JoinableGame):

    """
    Maps user commands to game mechanics and feedback.
    """

    def __init__(self, bot, ctx):
        super().__init__(ctx)
        self.blackjack = Blackjack()
        self.avatar_handler = BlackjackAvatarHandler()
        self.dealer = self.init_dealer(RollbotHost())
        self.dealer_name = self.dealer.display_name
        self.standing_players = []  # Match against the dealer's hand at the end of the game
        self.announcer = BlackjackAnnouncer(bot, self.dealer_name)
        self.dealer_executor = BlackjackDealer(self)
        self.max_time_left = 10 * 60  # 10 minutes
        self.results = {}

    def get_avatar(self, user) -> List[PlayerHand]:
        # Players own a list of hands: initially one hand, but can be multiple after a split
        return [PlayerHand()]

    def init_dealer(self, host) -> PlayerAvatar:
        if host is not None:
            return self.avatar_handler.create_avatar(host, Hand())

    async def start(self):
        self.dispense_cards()
        await self.show_player_cards()
        await self.dealer_executor.show_dealer_face_up()
        await self.check_initial_dealer_cards()

    def dispense_cards(self) -> None:

        def add_initial_cards(player: PlayerAvatar):
            starting_hand = self.avatar_handler.get_first_hand(player)
            num_cards = 2
            for i in range(num_cards):
                self.blackjack.deal_card(starting_hand)

        for player in self.players:
            add_initial_cards(player)

        add_initial_cards(self.dealer)

    async def show_player_cards(self) -> None:

        for player in self.players:
            await self.announce_cards(player)

    async def announce_cards(self, player):
        player_name = self.avatar_handler.get_name(player)
        hand = self.avatar_handler.get_first_hand(player)
        await self.announcer.player_cards(player_name, hand)

    async def check_initial_dealer_cards(self) -> None:
        is_game_end = await self.dealer_executor.is_dealer_blackjack()
        if is_game_end:
            await self.end_game()
        else:
            await self.trigger_next_turn()

    async def trigger_next_turn(self) -> None:
        are_player_turns_remaining = self.players
        if are_player_turns_remaining:
            await self.player_make_move()
        else:
            await self.check_dealer_turn()
            await self.end_game()

    async def check_dealer_turn(self) -> None:
        are_players_standing = self.standing_players
        if are_players_standing:
            await self.dealer_executor.dealer_make_move()
        else:
            await self.announcer.no_players_left()

    async def player_make_move(self) -> None:
        current_player = self.players[0]
        player_name = self.avatar_handler.get_name(current_player)
        hand = self.get_current_player_hand()
        await self.announcer.next_turn(player_name, hand)

    async def hit(self) -> None:
        hand = self.get_current_player_hand()
        new_card = self.blackjack.hit(hand)
        await self.announcer.report_hit(hand, new_card)
        await self.check_hit_bust()

    async def stand_current_hand(self) -> None:
        hand = self.get_current_player_hand()
        hand.end_turn()
        await self.announcer.progressing()
        await self.check_next_hand()

    async def attempt_double_down(self) -> None:
        hand = self.get_current_player_hand()
        if self.blackjack.double_down(hand):
            wager = hand.get_wager()
            await self.announcer.double_down_success(wager)
            await self.stand_current_hand()
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
            await self.trigger_next_turn()

    def current_player_stand(self) -> None:
        player = self.players.pop(0)
        self.standing_players.append(player)

    def get_current_player_hand(self) -> PlayerHand:
        hands = self.get_current_player_hands()
        return self._get_active_hand(hands)

    def get_current_player_hands(self) -> List[PlayerHand]:
        current_player = self.get_current_player()
        hands = self.avatar_handler.get_hands(current_player)
        return hands

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

    async def check_knock_out(self) -> None:
        current_player_has_hand = self.get_current_player_hands()
        if not current_player_has_hand:
            self.knock_out_current_player()
            await self.trigger_next_turn()
        else:
            await self.check_next_hand()

    async def end_game(self) -> None:
        """ Checks self.players in case the dealer has gotten a blackjack. """
        [await self.resolve_outcomes(player) for player in self.standing_players]
        [await self.resolve_outcomes(player) for player in self.players]
        self.in_progress = False

    async def resolve_outcomes(self, player) -> None:
        player_name = self.avatar_handler.get_name(player)
        hands = self.avatar_handler.get_hands(player)
        self.results[player] = 0
        for hand in hands:
            await self.announcer.player_hand(player_name, hand)
            hand_checker = BlackjackResultChecker(self, hand)
            await hand_checker.check_outcome()
            self.results[player] += hand.get_winnings() - hand.get_wager()

    def get_current_player(self) -> PlayerAvatar:
        return self.players[0]

    def knock_out_current_player(self) -> None:
        del self.players[0]

    @staticmethod
    def _get_active_hand(hands: List[PlayerHand]) -> PlayerHand:
        for hand in hands:
            if hand.is_active:
                return hand

    def get_dealer_hand(self) -> Hand:
        return self.avatar_handler.get_first_hand(self.dealer)