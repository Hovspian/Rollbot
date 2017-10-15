class Hand:
    def __init__(self):
        self.cards = []
        self.is_active = True
        self.plays_made = 0

    def stand(self):
        self.end_turn()

    def add_card(self, card):
        self.cards.append(card)
        self.plays_made += 1

    def end_turn(self):
        self.is_active = False
        self.plays_made += 1

    def get_first_card(self):
        return self.cards[0]


class PlayerHand(Hand):

    # Represents the user in Blackjack. A user can have multiple hands.

    def __init__(self, wager=10):
        super().__init__()
        self._wager = wager
        self._winnings = 0

    def get_wager(self) -> int:
        return self._wager

    def get_winnings(self) -> int:
        return self._winnings

    def double_down(self, card) -> None:
        self._wager *= 2
        self.add_card(card)
        self.end_turn()

    def split(self) -> dict:
        card = self.cards.pop(1)
        return card

    def blackjack_win(self) -> None:
        self._winnings += self._wager * 5

    def normal_win(self) -> None:
        self._winnings += self._wager * 3

    def lose(self) -> None:
        self._winnings -= self._wager
