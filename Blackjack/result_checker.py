from Blackjack.hand import PlayerHand


class BlackjackResultChecker:

    """
    Checks a single hand during end of game comparisons.
    """

    def __init__(self, executor, player_hand: PlayerHand):
        self.blackjack = executor.blackjack
        self.announcer = executor.announcer
        self.dealer_hand = executor.get_dealer_hand()
        self.player_hand = player_hand

    async def check_outcome(self) -> None:
        is_blackjack_win = self._is_blackjack_win()
        is_winner = await self._is_winner()
        is_standoff = self._is_stand_off()
        if is_blackjack_win:
            await self._resolve_blackjack_win()
        elif is_winner:
            await self._resolve_normal_win()
        elif is_standoff:
            await self._resolve_standoff()
        else:
            await self._resolve_loss()

    async def _resolve_blackjack_win(self):
        self.player_hand.blackjack_win()
        winnings = self.player_hand.get_winnings()
        await self.announcer.announce_player_blackjack(winnings)

    async def _resolve_normal_win(self):
        self.player_hand.normal_win()
        winnings = self.player_hand.get_winnings()
        await self.announcer.win(winnings)

    async def _resolve_standoff(self):
        self.player_hand.standoff()
        wager = self.player_hand.get_wager()
        await self.announcer.stand_off(wager)

    async def _resolve_loss(self):
        wager = self.player_hand.get_wager()
        await self.announcer.loss(wager)

    def _is_blackjack_win(self) -> bool:
        # Player wins if their hand is blackjack while the dealer's is not.
        is_dealer_blackjack = self.blackjack.is_blackjack(self.dealer_hand)
        is_player_blackjack = self.blackjack.is_blackjack(self.player_hand)
        return is_player_blackjack and not is_dealer_blackjack

    def _is_stand_off(self) -> bool:
        is_host_blackjack = self.blackjack.is_blackjack(self.dealer_hand)
        is_player_blackjack = self.blackjack.is_blackjack(self.player_hand)
        return is_player_blackjack and is_host_blackjack

    async def _is_winner(self) -> bool:
        player_busted = await self._check_bust()
        if player_busted:
            return False

        hand_value = self.player_hand.get_value()
        dealer_value = self._get_dealer_hand_value()
        return hand_value > dealer_value

    async def _check_bust(self) -> bool:
        if self.player_hand.is_bust():
            await self.announcer.declare_player_bust()
            return True

    def _get_dealer_hand_value(self):
        if self.dealer_hand.is_bust():
            self.dealer_hand.set_value(0)
        return self.dealer_hand.get_value()