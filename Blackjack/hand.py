class BlackjackHand:
    def __init__(self):
        self.is_active = True
        self.plays_made = 0  # Some actions depend on no plays being made.
        self._values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
                        '10': 10, 'J': 10, 'Q': 10, 'K': 10}
        self._cards = []
        self._value = 0  # The value of your cards.

    def hit(self, card) -> None:
        self.add_card(card)
        self.plays_made += 1

    def add_card(self, card) -> None:
        """
        Cards can be added without it necessarily being a player action.
        """
        self._cards.append(card)
        self._update_value()

    def end_turn(self):
        self.is_active = False
        self.plays_made += 1

    def set_value(self, value) -> None:
        self._value = value

    def get_value(self) -> int:
        return self._value

    def is_bust(self) -> bool:
        return self._value > 21

    def get_first_card(self) -> dict:
        return self._cards[0]

    def is_blackjack(self) -> bool:
        has_ace = False
        has_ten = False
        two_cards_in_hand = len(self._cards) == 2
        for card in self._cards:
            has_ace = self.is_ace(card)
            has_ten = self.is_ten_value(card)
        return two_cards_in_hand and has_ace and has_ten

    def is_ten_value(self, card) -> bool:
        """
        Jack, Queen, King have values of 10.
        """
        rank = card['rank']
        if rank in self._values:
            is_ten = self._values[rank] == 10
        else:
            is_ten = False
        return is_ten

    def _update_value(self) -> None:
        sum_values = sum([self.__calculate_value(card) for card in self._cards])
        value = self.__resolve_aces(sum_values)
        self.set_value(value)

    def __resolve_aces(self, sum_values: int) -> int:
        # Aces always add 1. Then, check if they can add 10 to make the full 11.

        aces = self.__get_aces()
        num_aces = len(aces)
        sum_values += num_aces

        for ace in aces:
            is_eleven_bust = (sum_values + 10) > 21
            if not is_eleven_bust:
                sum_values += 10

        return sum_values

    def __calculate_value(self, card) -> int:
        """
        Aces return a value of 0 and are handled elsewhere.
        """
        rank = card['rank']
        if rank in self._values:
            return self._values[rank]
        else:
            return 0

    def __get_aces(self) -> list:
        return list(filter(self.is_ace, self._cards))

    @staticmethod
    def is_ace(card) -> bool:
        rank = card['rank']
        return rank is 'A'


class PlayerHand(BlackjackHand):
    # Represents the user in Blackjack. A user can have multiple hands/representations.

    def __init__(self, wager=10):
        super().__init__()
        self._wager = wager
        self._winnings = 0

    def can_split(self) -> bool:
        two_cards = len(self._cards) == 2
        first_card = self._cards[0]
        second_card = self._cards[1]
        matching_rank = first_card['rank'] is second_card['rank']
        matching_values = self.__calculate_value(first_card) == self.__calculate_value(second_card)
        return (matching_rank or matching_values) and two_cards

    def get_wager(self) -> int:
        return self._wager

    def get_winnings(self) -> int:
        return self._winnings

    def double_down(self, card) -> None:
        self._wager *= 2
        self.hit(card)

    def split(self) -> dict:
        card = self._cards.pop(1)
        super()._update_value()
        return card

    def blackjack_win(self) -> None:
        self._winnings += self._wager * 5

    def normal_win(self) -> None:
        self._winnings += self._wager * 3
