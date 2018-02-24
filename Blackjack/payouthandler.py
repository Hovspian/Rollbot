from Blackjack.hand import PlayerHand
from Blackjack.player import BlackjackPlayer
from Blackjack.result_checker import BlackjackResultChecker


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