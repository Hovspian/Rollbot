import random
import math
from typing import List
from Slots.result_checker import ResultChecker
from Slots.slots_feedback import SlotsFeedback


class SlotMachine:
    def __init__(self):
        self.num_columns = 3
        self.payout_multiplier = 1
        self.default_outcomes = []
        self.bias_index = 0
        self.init_reel_size = int(math.ceil(self.num_columns * 1.5))
        self.reels = []
        self.results = []
        self.winning_symbols = []
        self.winning_combos = []
        self.payout_amount = 0
        self.bias_direction = self._get_default_bias

    def play_slot(self) -> None:
        self._roll_first_column()

        def _perform_rolls():
            self._add_result(self._roll_next_column())

        [_perform_rolls() for i in range(self.num_columns - 1)]
        self._check_results()

    def draw_slot_interface(self) -> str:
        rows = self.get_rows()

        def get_emotes(symbols) -> str:
            return ''.join([symbol['emote'] for symbol in symbols])
        return '\n'.join([get_emotes(row) for row in rows])

    def get_outcome_report(self) -> str:
        return SlotsFeedback(self).get_outcome_report()

    def get_rows(self) -> List[list]:
        def _get_row(i):
            return [self.results[column][i] for column in range(self.num_columns)]
        return [_get_row(i) for i in range(self.num_columns)]

    def _get_default_bias(self):
        return self.bias_index

    def _roll_first_column(self):
        self._roll_initial_reel()
        self._roll_bias_index()
        first_column = self._roll_column(self._get_first_reel())
        self._add_result(first_column)

    def _get_first_reel(self):
        return self.reels[0]

    def _check_results(self):
        result_checker = ResultChecker(self)
        result_checker.analyze_results()
        self.payout_amount += result_checker.calculate_payout()

    def _roll_initial_reel(self):
        self.reels.append(self._roll_reel(self.default_outcomes))

    def get_bias_options(self):
        first_row = 0
        last_row = self.num_columns - 1
        random_index = random.randint(first_row, last_row)
        no_bias = -1
        return [random_index, random_index, random_index, no_bias, no_bias]

    def _roll_bias_index(self):
        first_row = 0
        last_row = self.num_columns - 1
        self.bias_index = self._roll(self.get_bias_options())
        if self.bias_index == first_row:
            self._roll_bias_direction(self._top_left_diagonal)
        elif self.bias_index == last_row:
            self._roll_bias_direction(self._top_right_diagonal)

    def _roll_bias_direction(self, diagonal):
        bias_directions = [self.bias_direction, diagonal, diagonal]
        self.bias_direction = self._roll(bias_directions)

    def _roll_reel(self, symbols):
        reel = []

        def roll_add_to_reel(i):
            previous_symbol = has_previous_symbol(i)
            if previous_symbol:
                filtered_container = self.remove_symbol(symbols, previous_symbol)
                symbol = self._roll(filtered_container)
            else:
                symbol = self._roll(symbols)
            reel.append(symbol)

        def has_previous_symbol(i):
            if len(reel) > 0:
                return reel[i - 1]

        [roll_add_to_reel(i) for i in range(self.init_reel_size)]
        return reel

    def _add_result(self, column) -> None:
        self.results.append(column)

    def _roll_next_column(self):
        reel = self._rebuild_reel()
        if self._has_bias():
            match_index = self._get_match_index(reel)
            return self._roll_column(reel, match_index)
        return self._roll_column(reel)

    def _has_bias(self):
        return self.bias_index > -1

    def _rebuild_reel(self):
        first_column = self.results[0]
        exclude_symbols = self.num_columns
        new_reel = self._roll_reel(self._get_first_reel())
        self.reels.append(new_reel)
        return new_reel[:exclude_symbols] + first_column

    def _roll_column(self, reel, index=0) -> List[dict]:
        column = []
        for i in range(self.num_columns):
            column.append(reel[index])
            index = self._loop_reel_value(index + 1)
        return column

    def _get_match_index(self, reel):
        first_column = self.results[0]
        symbol_to_match = first_column[self.bias_index]
        return reel.index(symbol_to_match) - self.bias_direction()

    def _top_left_diagonal(self):
        index = self.bias_index + len(self.results)
        return self._loop_reel_value(index)

    def _top_right_diagonal(self):
        index = self.bias_index - len(self.results)
        return self._loop_reel_value(index)

    def _loop_reel_value(self, index):
        previous = len(self.reels) - 1
        previous_reel_size = len(self.reels[previous])
        if index > previous_reel_size - 1:
            return index - previous_reel_size
        if index < 0:
            return previous_reel_size + index
        return index

    @staticmethod
    def remove_symbol(container, filter_symbol):
        return [symbol for symbol in container if symbol != filter_symbol]

    @staticmethod
    def _roll(input_list: List) -> any:
        pick = random.randint(0, len(input_list) - 1)
        return input_list[pick]
