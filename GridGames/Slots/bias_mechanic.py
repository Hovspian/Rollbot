from helper_functions import *


class SlotsBias:
    def __init__(self, slot_machine):
        self.bias_index = 0
        self.bias_direction = self.row_bias
        self.slot_machine = slot_machine
        self.num_columns = slot_machine.num_columns
        self.first_row = 0
        self.last_row = self.num_columns - 1
        self.results = slot_machine.results

    def initialize(self) -> None:
        self._roll_bias_index()
        self._check_bias_directions()

    def get_index(self, reel) -> int:
        if self._has_bias() and self.results:
            index = self.get_match_index(reel)
        else:
            random_index = random.randint(0, len(reel) - 1)
            index = random_index
        return index

    def get_match_index(self, reel) -> int:
        first_column = self.results[0]
        symbol_to_match = first_column[self.bias_index]
        bias_direction = self.bias_direction()
        align_to_bias = loop_list_value(index=bias_direction, container=reel)
        return reel.index(symbol_to_match) - align_to_bias

    def _get_bias_options(self) -> List[int]:
        # Reels may align themselves to match a chosen symbol in the first column
        random_index = random.randint(self.first_row, self.last_row)
        no_bias = -1
        return [random_index, random_index, no_bias]

    def _roll_bias_index(self) -> None:
        bias_options = self._get_bias_options()
        self.bias_index = roll(bias_options)

    def _check_bias_directions(self):
        # If index bias has potential to be diagonal, roll so the winning outcome may still be a row
        diagonal_bias = self.get_diagonal_bias()
        if diagonal_bias is not None:
            self._roll_bias_direction(diagonal_bias)

    def get_diagonal_bias(self) -> classmethod:
        if self.bias_index == self.first_row:
            return self._top_left_diagonal_bias
        elif self.bias_index == self.last_row:
            return self._top_right_diagonal_bias

    def _roll_bias_direction(self, diagonal) -> None:
        # Store chosen bias direction method
        row = self.row_bias
        bias_directions = [row, diagonal, diagonal]
        self.bias_direction = roll(bias_directions)

    def _has_bias(self) -> bool:
        no_bias = -1
        return self.bias_index > no_bias

    def row_bias(self) -> int:
        return self.bias_index

    def _top_left_diagonal_bias(self) -> int:
        index = self.bias_index + len(self.results)
        return index

    def _top_right_diagonal_bias(self) -> int:
        index = self.bias_index - len(self.results)
        return index
