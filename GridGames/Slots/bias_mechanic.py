from typing import List
import random


class SlotsBias:
    def __init__(self, slot_machine):
        self.bias_index = 0
        self.bias_direction = self.row_bias
        self.slot_machine = slot_machine
        self.num_columns = slot_machine.num_columns
        self.first_row = 0
        self.last_row = self.num_columns - 1
        self.results = slot_machine.results
        # TODO move me
        self._roll = slot_machine._roll
        self._loop_reel_value = slot_machine._loop_reel_value

    def initialize(self):
        self._roll_bias_index()
        self._check_bias_directions()

    def get_index(self, reel):
        if self._has_bias() and self.results:
            index = self.get_match_index(reel)
        else:
            index = random.randint(0, len(reel) - 1)
        return index

    def get_match_index(self, reel) -> int:
        first_column = self.results[0]
        symbol_to_match = first_column[self.bias_index]
        return reel.index(symbol_to_match) - self.bias_direction()

    def _get_bias_options(self) -> List[int]:
        # Reels may align themselves to a chosen symbol in the first column
        random_index = random.randint(self.first_row, self.last_row)
        no_bias = -1
        return [random_index, random_index, no_bias]

    def _roll_bias_index(self) -> None:
        bias_options = self._get_bias_options()
        self.bias_index = self._roll(bias_options)

    def _check_bias_directions(self):
        # If index bias has potential to be diagonal, roll so that the winning outcome may still be a row
        diagonal_bias = self.get_diagonal_bias()
        if diagonal_bias:
            self._roll_bias_direction(diagonal_bias)

    def get_diagonal_bias(self):
        if self.bias_index == self.first_row:
            return self._top_left_diagonal
        elif self.bias_index == self.last_row:
            return self._top_right_diagonal

    def _roll_bias_direction(self, diagonal):
        row = self.row_bias
        bias_directions = [row, diagonal, diagonal]
        self.bias_direction = self._roll(bias_directions)

    def _has_bias(self):
        no_bias = -1
        return self.bias_index > no_bias

    def row_bias(self):
        return self.bias_index

    def _top_left_diagonal(self) -> int:
        index = self.bias_index + len(self.results)
        return self._loop_reel_value(index)

    def _top_right_diagonal(self) -> int:
        index = self.bias_index - len(self.results)
        return self._loop_reel_value(index)
