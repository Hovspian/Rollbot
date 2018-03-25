from Blackjack.payout_handler import PayoutHandler
from Blackjack.player import BlackjackPlayer
from Blackjack.announcer import BlackjackPlayerAnnouncer
from Blackjack.deck import Deck
from Blackjack.dealer import BlackjackDealer
from Blackjack.hand import BlackjackHand, PlayerHand
from Core.core_game_class import GameCore
from Core.constants import GAME_ID


class Blackjack(GameCore):

    def __init__(self, bot, ctx):
        super().__init__(ctx)
        self.deck = Deck()
        self.bot = bot
        self.announcer = BlackjackPlayerAnnouncer(bot)
        self.dealer = self.init_dealer()
        self.standing_players = []  # Players to compare with the dealer's hand at the end of the game.
        self.max_time_left = 10 * 60  # 10 minutes
        self.payouts = []
        self.id = GAME_ID['BLACKJACK']
        self.payout_handler = PayoutHandler(self)
        self.max_num_players = 5

    def init_dealer(self) -> BlackjackDealer:
        # TODO let players host blackjack games
        user = self.bot.user
        return BlackjackDealer(user, self)

    async def start_game(self):
        super().start_game()
        self.__dispense_cards()
        await self.__show_player_cards()
        await self.dealer.show_face_up()
        await self.__check_initial_dealer_cards()

    def add_user(self, user):
        super().add_user(user)
        self.add_player(user)

    def add_player(self, user) -> None:
        player = BlackjackPlayer(user)
        super().add_player(player)

    def is_turn(self, user):
        first_in_queue = self.__get_current_player().user
        return user is first_in_queue

    async def hit(self) -> None:
        hand = self.__get_current_player().get_active_hand()
        new_card = self.deck.draw_card()
        hand.hit(new_card)
        await self.announcer.report_hit(hand, new_card)
        await self.__check_hit_bust(hand)

    async def stand_current_hand(self) -> None:
        hand = self.__get_current_player().get_active_hand()
        hand.end_turn()
        await self.announcer.progressing()
        await self.__check_next_hand()

    async def attempt_double_down(self) -> None:
        hand = self.__get_current_player().get_active_hand()
        if self._double_down(hand):
            wager = hand.get_wager()
            await self.announcer.double_down_success(wager)
            await self.stand_current_hand()
        else:
            await self.announcer.double_down_fail()

    async def attempt_split(self) -> None:
        player = self.__get_current_player()
        hand = player.get_active_hand()
        if player.split_hand():
            await self.announcer.split_successful(hand)
        else:
            await self.announcer.split_fail()

    def get_payouts(self):
        return self.payouts

    def _double_down(self, hand: PlayerHand) -> bool:
        """
        Double wager, then draw and finish.
        """
        if hand.can_double_down():
            card = self.deck.draw_card()
            hand.double_down(card)
            return True

    async def end_game(self) -> None:
        await self.payout_handler.resolve_outcomes()
        self.payouts = self.payout_handler.get_payouts()
        super().end_game()

    def __dispense_cards(self) -> None:
        for player in self.players:
            self.__add_initial_cards(player)
        self.__add_initial_cards(self.dealer)

    def __add_initial_cards(self, participant):
        starting_hand = participant.get_active_hand()
        num_cards = 2
        for i in range(num_cards):
            card = self.deck.draw_card()
            starting_hand.add_card(card)

    async def __show_player_cards(self) -> None:
        for player in self.players:
            hand = player.get_active_hand()
            await self.announcer.player_cards(player.name, hand)

    async def __check_initial_dealer_cards(self) -> None:
        if await self.dealer.has_blackjack():
            await self.end_game()
        else:
            await self.__next_turn()

    async def __next_turn(self) -> None:
        are_player_turns_remaining = self.players
        if are_player_turns_remaining:
            await self.__next_player_turn()
        else:
            await self.__check_dealer_turn()
            await self.end_game()

    async def __check_dealer_turn(self) -> None:
        are_players_standing = self.standing_players
        if are_players_standing:
            await self.dealer.make_move()
        else:
            await self.announcer.no_players_left()

    async def __next_player_turn(self) -> None:
        current_player = self.players[0]
        player_name = current_player.name
        hand = self.__get_current_player().get_active_hand()
        await self.announcer.next_turn(player_name, hand)

    async def __check_next_hand(self) -> None:
        active_hand = self.__get_current_player().get_active_hand()
        if active_hand:
            await self.announcer.next_hand_options(active_hand)
        else:
            self.__current_player_stand()
            await self.__next_turn()

    def __current_player_stand(self) -> None:
        """
        When a player stands, their turn ends. Hands are compared at the end of the game.
        """
        player = self.players.pop(0)
        self.standing_players.append(player)

    async def __check_hit_bust(self, hand: BlackjackHand) -> None:
        if not hand.is_bust():
            await self.announcer.ask_hit_again()
            return
        await self.announcer.declare_player_bust()
        await self.__bust_current_hand()

    async def __bust_current_hand(self) -> None:
        player = self.__get_current_player()
        hand_to_bust = player.bust_active_hand()
        self.payout_handler.add_bust(player, hand_to_bust)
        await self.__check_knock_out()

    async def __check_knock_out(self) -> None:
        """
        A player is removed from the game if they have no valid hands remaining.
        """
        if self.__get_current_player().get_hands():
            await self.__check_next_hand()
        else:
            self.__knock_out_current_player()
            await self.__next_turn()

    def __get_current_player(self) -> BlackjackPlayer:
        """
        The player whose turn it is.
        """
        return self.players[0]

    def __knock_out_current_player(self) -> None:
        del self.players[0]

