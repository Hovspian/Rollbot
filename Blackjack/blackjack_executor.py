from Core.player_avatar import *
from Blackjack.announcer import BlackjackAnnouncer
from Blackjack.blackjack_mechanics import BlackjackMechanics
from Blackjack.dealer import BlackjackDealer
from Blackjack.hand import Hand, PlayerHand
from Blackjack.result_checker import BlackjackResultChecker
from Core.core_game_class import GameCore
from Core.constants import GAME_ID


class BlackjackExecutor(GameCore):
    """ 'When' Blackjack rules are applied """

    def __init__(self, bot, ctx):
        super().__init__(ctx)
        self.blackjack = BlackjackMechanics()
        self.bot = bot
        self.dealer = self.init_dealer()
        self.dealer_name = self.dealer.name
        self.standing_players = []  # Match against the dealer's hand at the end of the game
        self.announcer = BlackjackAnnouncer(bot, self.dealer_name)
        self.dealer_executor = BlackjackDealer(self)
        self.max_time_left = 10 * 60  # 10 minutes
        self.payouts = []
        self.id = GAME_ID['BLACKJACK']

    def init_dealer(self) -> BlackjackAvatar:
        # TODO let players host blackjack games
        user = self.bot.user
        dealer_avatar = self._get_dealer_avatar()
        return BlackjackAvatar(user, dealer_avatar)

    async def start_game(self):
        super().start_game()
        self.dispense_cards()
        await self.show_player_cards()
        await self.dealer_executor.show_dealer_face_up()
        await self.check_initial_dealer_cards()

    def dispense_cards(self) -> None:
        for player in self.players:
            self.add_initial_cards(player)
        self.add_initial_cards(self.dealer)

    def add_initial_cards(self, player: BlackjackAvatar):
        starting_hand = player.get_first_hand()
        num_cards = 2
        for i in range(num_cards):
            self.blackjack.deal_card(starting_hand)

    async def show_player_cards(self) -> None:
        for player in self.players:
            await self.announce_cards(player)

    async def announce_cards(self, player):
        hand = player.get_first_hand()
        await self.announcer.player_cards(player.name, hand)

    async def check_initial_dealer_cards(self) -> None:
        is_game_end = await self.dealer_executor.is_dealer_blackjack()
        if is_game_end:
            await self.end_game()
        else:
            await self.trigger_next_turn()

    async def trigger_next_turn(self) -> None:
        are_player_turns_remaining = self.players
        if are_player_turns_remaining:
            await self.player_turn()
        else:
            await self.check_dealer_turn()
            await self.end_game()

    async def check_dealer_turn(self) -> None:
        are_players_standing = self.standing_players
        if are_players_standing:
            await self.dealer_executor.dealer_make_move()
        else:
            await self.announcer.no_players_left()

    async def player_turn(self) -> None:
        current_player = self.players[0]
        player_name = current_player.name
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
        hands = current_player.get_hands()
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
        # Checks self.players in case the dealer has gotten a blackjack.
        [await self.resolve_outcomes(player) for player in self.standing_players]
        [await self.resolve_outcomes(player) for player in self.players]
        super().end_game()

    async def resolve_outcomes(self, player: BlackjackAvatar) -> None:
        hands = player.get_hands()
        for hand in hands:
            await self.announcer.player_hand(player.name, hand)
            hand_checker = BlackjackResultChecker(self, hand)
            await hand_checker.check_outcome()
            self.payouts.append({
                'to_user': player.user,
                'gold_difference': hand.get_winnings(),
                'from_user': self.dealer
            })

    def get_current_player(self) -> BlackjackAvatar:
        return self.players[0]

    def knock_out_current_player(self) -> None:
        del self.players[0]

    def get_dealer_hand(self) -> Hand:
        return self.dealer.get_first_hand()

    def add_user(self, user):
        super().add_user(user)
        self.add_player(user)

    def add_player(self, user) -> None:
        # Couples the avatar and user in a PlayerAvatar class
        avatar = self.get_avatar()
        player_avatar = BlackjackAvatar(user, avatar)
        super().add_player(player_avatar)

    @staticmethod
    def _get_active_hand(hands: List[PlayerHand]) -> PlayerHand:
        return next(hand for hand in hands if hand.is_active)

    @staticmethod
    def get_avatar() -> List[PlayerHand]:
        # Players own a list of hands: initially one hand, but can be multiple after a split.
        return [PlayerHand()]

    @staticmethod
    def _get_dealer_avatar() -> List[Hand]:
        # Dealers do not have many of the options that players do.
        return [Hand()]
