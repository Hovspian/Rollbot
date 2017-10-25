class BlackjackDealer:
    def __init__(self, executor):
        self.dealer_hand = executor.get_dealer_hand()
        self.blackjack = executor.blackjack
        self.announcer = executor.announcer

    async def show_dealer_face_up(self):
        first_card = self.dealer_hand.get_first_card()
        await self.announcer.dealer_card(first_card)

    async def is_dealer_blackjack(self) -> bool:
        ace_or_ten = await self._is_ace_or_ten()
        dealer_blackjack = await self._check_blackjack()
        return ace_or_ten and dealer_blackjack

    async def dealer_make_move(self) -> None:
        await self.announcer.dealer_turn(self.dealer_hand)
        await self._dealer_hit_loop()
        await self._dealer_turn_end()

    async def _check_dealer_bust(self) -> bool:
        if self.dealer_hand.is_bust():
            await self.announcer.declare_dealer_bust()
            return True

    async def _dealer_hit_loop(self) -> None:
        while self.dealer_hand.get_value() < 17:
            card = self.blackjack.hit(self.dealer_hand)
            await self.announcer.dealer_hit(card)

    async def _is_ace_or_ten(self) -> bool:
        first_card = self.dealer_hand.get_first_card()
        is_ace = self.blackjack.is_ace(first_card)
        is_ten = self.blackjack.is_ten_value(first_card)
        if is_ace or is_ten:
            await self.announcer.ace_or_ten_message(self.dealer_hand)
            return True

    async def _dealer_turn_end(self) -> None:
        is_blackjack = await self._check_blackjack()
        is_bust = await self._check_dealer_bust()
        if not is_blackjack and not is_bust:
            await self.announcer.dealer_stand()

    async def _check_blackjack(self) -> bool:
        if self.blackjack.is_blackjack(self.dealer_hand):
            await self.announcer.announce_blackjack()
            return True