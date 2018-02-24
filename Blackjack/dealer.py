from Blackjack.announcer import BlackjackDealerAnnouncer
from Blackjack.hand import BlackjackHand


class BlackjackDealer:

    """
    Dealer AI.
    """

    def __init__(self, user, game):
        self.user = user
        self.name = user.display_name
        self.deck = game.deck
        self._hand = BlackjackHand()
        self.announcer = BlackjackDealerAnnouncer(game.bot, user.display_name)

    def get_active_hand(self):
        return self._hand

    async def show_face_up(self):
        first_card = self._hand.get_first_card()
        await self.announcer.dealer_card(first_card)

    async def has_blackjack(self) -> bool:
        """
        At game start, the dealer reveals a card which may need to be checked for a blackjack.
        """
        await self.__check_ace_or_ten()
        return await self.__check_blackjack()

    async def make_move(self) -> None:
        await self.announcer.dealer_turn(self._hand)
        await self.__hit_loop()
        await self.__end_turn()

    async def __hit_loop(self) -> None:
        """
        Continue drawing cards until the hand has a value of 17+.
        """
        while self._hand.get_value() < 17:
            card = self.deck.draw_card()
            self._hand.hit(card)
            await self.announcer.dealer_hit(card)

    async def __check_ace_or_ten(self) -> bool:
        first_card = self._hand.get_first_card()
        is_ace = self._hand.is_ace(first_card)
        is_ten = self._hand.is_ten_value(first_card)
        if is_ace or is_ten:
            await self.announcer.ace_or_ten_message(self._hand)
            return True

    async def __end_turn(self) -> None:
        is_blackjack = await self.__check_blackjack()
        is_bust = await self.__check_bust()
        if not is_blackjack and not is_bust:
            await self.announcer.dealer_stand()

    async def __check_blackjack(self) -> bool:
        if self._hand.is_blackjack():
            await self.announcer.announce_blackjack()
            return True

    async def __check_bust(self) -> bool:
        if self._hand.is_bust():
            await self.announcer.declare_dealer_bust()
            return True
