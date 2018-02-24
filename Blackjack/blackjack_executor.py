from Blackjack.player import BlackjackPlayer
from Core.player_avatar import *
from Blackjack.announcer import BlackjackPlayerAnnouncer
from Blackjack.deck import Deck
from Blackjack.dealer import BlackjackDealer
from Blackjack.hand import BlackjackHand, PlayerHand
from Blackjack.result_checker import BlackjackResultChecker
from Core.core_game_class import GameCore
from Core.constants import GAME_ID


class Blackjack(GameCore):
    """
    'When' Blackjack rules are applied.
    """

    def __init__(self, bot, ctx):
        super().__init__(ctx)
        self.deck = Deck()
        self.bot = bot
        self.announcer = BlackjackPlayerAnnouncer(bot)
        self.dealer = self.init_dealer()
        self.standing_players = []  # Match against the dealer's hand at the end of the game
        self.max_time_left = 10 * 60  # 10 minutes
        self.payouts = []
        self.id = GAME_ID['BLACKJACK']
        self.payout_handler = PayoutHandler(self)

    def init_dealer(self) -> BlackjackDealer:
        # TODO let players host blackjack games
        dealer = self.bot.user
        return BlackjackDealer(dealer, self)

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
        new_card = self.deck.hit(hand)
        await self.announcer.report_hit(hand, new_card)
        self.__check_hit_bust(hand)

    async def stand_current_hand(self) -> None:
        hand = self.__get_current_player().get_active_hand()
        hand.end_turn()
        await self.announcer.progressing()
        await self.__check_next_hand()

    async def attempt_double_down(self) -> None:
        hand = self.__get_current_player().get_active_hand()
        if self.deck.double_down(hand):
            wager = hand.get_wager()
            await self.announcer.double_down_success(wager)
            await self.stand_current_hand()
        else:
            await self.announcer.double_down_fail()

    async def attempt_split(self) -> None:
        player = self.__get_current_player()
        hand = player.get_active_hand()
        if self.split(player, hand):
            await self.announcer.split_successful(hand)
        else:
            await self.announcer.split_fail()

    @staticmethod
    def split(player: BlackjackPlayer, hand) -> bool:
        """
        If two cards are the same value, split them into two hands
        """
        hands = player.get_hands()
        within_max_num_hands = len(hands) == 1
        if within_max_num_hands and hand.can_split():
            split_card = hand.split()
            new_hand = PlayerHand()
            new_hand.add_card(split_card)
            hands.append(new_hand)
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
            self.deck.deal_card(starting_hand)

    async def __show_player_cards(self) -> None:
        for player in self.players:
            hand = player.get_first_hand()
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
        hand_to_bust = player.bust_current_hand()
        self.payout_handler.bust(player, hand_to_bust)
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
        return self.players[0]

    def __knock_out_current_player(self) -> None:
        del self.players[0]


class PayoutHandler:
    def __init__(self, game):
        self.game = game
        self.announcer = game.announcer
        self._payouts = []
        self.dealer = game.dealer

    def get_payouts(self):
        return self._payouts

    async def resolve_outcomes(self):
        for player in self.game.standing_players:
            await self.__resolve(player)
        # Check self.players in case the dealer has gotten a blackjack.
        for player in self.game.players:
            await self.__resolve(player)

    def bust(self, player: BlackjackPlayer, hand: PlayerHand):
        wager = hand.get_wager()
        self.__add_player_loss_payout(player, wager)

    async def __resolve(self, player: BlackjackPlayer) -> None:
        hands = player.get_hands()
        for hand in hands:
            await self.announcer.player_hand(player.name, hand)
            hand_checker = BlackjackResultChecker(self, hand)
            await hand_checker.check_outcome()
            if hand_checker.is_winner:
                self.__add_payout(player.user, hand.get_winnings(), self.dealer.user)
            elif hand_checker.is_loser:
                wager = hand.get_wager()
                self.__add_player_loss_payout(player, wager)

    def __add_payout(self, to_user, amount, from_user):
        self._payouts.append({
            'to_user': to_user,
            'amount': amount,
            'from_user': from_user
        })

    def __add_player_loss_payout(self, player: BlackjackPlayer, wager: int):
        to_dealer = self.dealer.user
        from_user = player.user
        self.__add_payout(to_dealer, wager, from_user)