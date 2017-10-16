from typing import List


class Hand:
    def __init__(self):
        self._cards = []
        self.is_active = True
        self.plays_made = 0
        self._value = 0

    def hit(self, card):
        self.add_card(card)
        self.plays_made += 1

    def add_card(self, card):
        self._cards.append(card)

    def end_turn(self):
        self.is_active = False
        self.plays_made += 1

    def get_first_card(self):
        return self._cards[0]

    def update_value(self, value):
        self._value = value

    def get_value(self):
        return self._value

    def is_bust(self) -> bool:
        return self._value > 21

    def get_cards(self) -> List[dict]:
        return self._cards

    def can_make_turn(self) -> bool:
        return self.is_active


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
        self.hit(card)

    def split(self) -> dict:
        card = self._cards.pop(1)
        return card

    def blackjack_win(self) -> None:
        self._winnings += self._wager * 5

    def normal_win(self) -> None:
        self._winnings += self._wager * 3

    def lose(self) -> None:
        self._winnings -= self._wager
