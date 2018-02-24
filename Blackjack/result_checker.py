from Blackjack.hand import PlayerHand


class BlackjackResultChecker:

    """
    Compare a hand to the dealer's.
    """

    def __init__(self, game, player_hand: PlayerHand):
        self.announcer = game.announcer
        self.dealer_hand = game.get_dealer_hand()
        self.player_hand = player_hand
        self.is_winner = False
        self.is_loser = False

    async def check_outcome(self) -> None:
        if self._is_blackjack():
            await self._resolve_blackjack_win()
        elif await self._is_winner():
            await self._resolve_normal_win()
        elif self._is_stand_off():
            await self._resolve_standoff()
        else:
            await self._resolve_loss()

    async def _resolve_blackjack_win(self):
        self.is_winner = True
        self.player_hand.blackjack_win()
        winnings = self.player_hand.get_winnings()
        await self.announcer.announce_player_blackjack(winnings)

    async def _resolve_normal_win(self):
        self.is_winner = True
        self.player_hand.normal_win()
        winnings = self.player_hand.get_winnings()
        await self.announcer.win(winnings)

    async def _resolve_standoff(self):
        wager = self.player_hand.get_wager()
        await self.announcer.stand_off(wager)

    async def _resolve_loss(self):
        self.is_loser = True
        wager = self.player_hand.get_wager()
        await self.announcer.loss(wager)

    def _is_blackjack(self) -> bool:
        # Player wins if their hand is blackjack while the dealer's is not.
        is_dealer_blackjack = self.dealer_hand.is_blackjack()
        is_player_blackjack = self.player_hand.is_blackjack()
        return is_player_blackjack and not is_dealer_blackjack

    def _is_stand_off(self) -> bool:
        is_host_blackjack = self.dealer_hand.is_blackjack()
        is_player_blackjack = self.player_hand.is_blackjack()
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
            return 0
        return self.dealer_hand.get_value()