from GridGames.ScratchCard.scratch_card import ScratchCard
from GridGames.helper_functions import *
from GridGames.ScratchCard.constants import *
from GridGames.ScratchCard.Hammerpot.render_hammerpot import RenderHammerpot
from GridGames.ScratchCard.Hammerpot.feedback import HammerpotFeedback
from typing import List
import random


class Hammerpot(ScratchCard):
    def __init__(self):
        super().__init__()
        self.max_time_left = 180
        self.attempts_remaining = 3
        self.underlying_symbols = [ONE, TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE]
        self.possible_payouts = [1, 3, 5, 10, 15, 25, 50, 75, 100, 150, 200]
        self.payouts = {}
        self.chosen_sum = 0
        self.announcement = HammerpotFeedback(self)

    def initialize_card(self):
        super().initialize_card()
        [self._link_sum_to_payout(sum_value) for sum_value in self._get_card_sums()]
        self._reveal_random_tile()
        self.card_render = RenderHammerpot(self)

    def pick_line(self, line: List[list]):
        self._reveal_line(line)
        tiles = self._get_tiles(line)
        self.chosen_sum = self._get_chosen_sum(tiles)
        self._end_game()

    def _end_game(self):
        self.winnings = self._get_payout()
        self.in_progress = False

    def _reveal_line(self, line):
        for coordinates in line:
            y = coordinates[0]
            x = coordinates[1]
            self._scratch(y, x)

    def _reveal_random_tile(self):

        def random_coordinate():
            return random.randint(0, self.num_columns - 1)
        y = random_coordinate()
        x = random_coordinate()
        self._reveal_tile(y, x)

    def _get_tiles(self, list_coordinates):
        def get_tile(coordinates):
            y = coordinates[0]
            x = coordinates[1]
            return self.underlying_symbols[y][x]
        return [get_tile(coordinates) for coordinates in list_coordinates]

    def _get_card_sums(self):
        # Returns all unique sums of each column, row and diagonal on the card
        winnable_sums = []
        top_left_diagonal = self._get_top_left_diagonal_tiles()
        top_right_diagonal = self._get_top_right_diagonal_tiles()
        random.shuffle(self.possible_payouts)

        def _add_sum(symbols):
            value_sum = self._get_chosen_sum(symbols)
            if value_sum not in winnable_sums:
                winnable_sums.append(value_sum)

        [_add_sum(column) for column in self.underlying_symbols]
        [_add_sum(row) for row in self.get_rows(self.underlying_symbols)]
        _add_sum(top_left_diagonal)
        _add_sum(top_right_diagonal)
        return winnable_sums

    def _get_top_left_diagonal_tiles(self) -> List[dict]:
        return self._get_diagonal(self.underlying_symbols)

    def _get_top_right_diagonal_tiles(self) -> List[dict]:
        reversed_columns = reversed(self.underlying_symbols)
        return self._get_diagonal(reversed_columns)

    @staticmethod
    def _get_diagonal(columns) -> List[dict]:
        return [column[i] for i, column in enumerate(columns)]

    def _get_chosen_sum(self, symbols):
        return sum([self.get_value(symbol) for symbol in symbols])

    def _link_sum_to_payout(self, sum_value):
        first_payout_value = self.possible_payouts[0]
        self.payouts[sum_value] = first_payout_value
        self.possible_payouts = remove_value(self.possible_payouts, first_payout_value)

    def _get_payout(self):
        return self.payouts[self.chosen_sum]