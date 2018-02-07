class BlackjackDealer:

    """
    Dealer AI mechanics.
    """

    def __init__(self, executor):
        self.hand = executor.get_dealer_hand()
        self.blackjack = executor.blackjack
        self.announcer = executor.announcer

    async def show_face_up(self):
        first_card = self.hand.get_first_card()
        await self.announcer.dealer_card(first_card)

    async def is_blackjack(self) -> bool:
        ace_or_ten = await self.__is_ace_or_ten()
        dealer_blackjack = await self.__check_blackjack()
        return ace_or_ten and dealer_blackjack

    async def make_move(self) -> None:
        await self.announcer.dealer_turn(self.hand)
        await self.hit_loop()
        await self.__end_turn()

    async def check_bust(self) -> bool:
        if self.hand.is_bust():
            await self.announcer.declare_dealer_bust()
            return True

    async def hit_loop(self) -> None:
        """
        Continue drawing cards until the hand has a value of 17, or is busted.
        """
        while self.hand.get_value() < 17:
            card = self.blackjack.hit(self.hand)
            await self.announcer.dealer_hit(card)

    async def __is_ace_or_ten(self) -> bool:
        """
        At game start, the dealer reveals a card which may need to be checked for a blackjack.
        """
        first_card = self.hand.get_first_card()
        is_ace = self.blackjack.is_ace(first_card)
        is_ten = self.blackjack.is_ten_value(first_card)
        if is_ace or is_ten:
            await self.announcer.ace_or_ten_message(self.hand)
            return True

    async def __end_turn(self) -> None:
        is_blackjack = await self.__check_blackjack()
        is_bust = await self.check_bust()
        if not is_blackjack and not is_bust:
            await self.announcer.dealer_stand()

    async def __check_blackjack(self) -> bool:
        if self.blackjack.is_blackjack(self.hand):
            await self.announcer.announce_blackjack()
            return True
