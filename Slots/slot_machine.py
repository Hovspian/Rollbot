import random
from typing import List
from Slots.result_checker import ResultChecker
from Slots.slots_feedback import SlotsFeedback


class SlotMachine:
    def __init__(self):
        self.num_columns = 3
        self.payout_multiplier = 1
        self.results = []
        self.winning_symbols = []
        self.winning_combos = []
        self.default_outcomes = []
        self.reel = []
        self.bias_index = 0

    def play_slot(self) -> None:
        self.reel = self.roll_reel(self.default_outcomes)
        self.bias_index = random.randint(0, self.num_columns - 1)

        def _perform_rolls():
            self._add_result(self._roll_column())

        [_perform_rolls() for i in range(self.num_columns)]
        ResultChecker(self).analyze_results()

    def draw_slot_interface(self) -> str:
        rows = self.get_rows()

        def get_emotes(symbols) -> str:
            return ''.join([symbol['emote'] for symbol in symbols])

        return '\n'.join([get_emotes(row) for row in rows])

    def get_outcome_report(self) -> str:
        return SlotsFeedback(self).get_outcome_report()

    def get_payout(self):
        return SlotsFeedback(self).get_payout()

    @staticmethod
    def get_lose_message() -> str:
        return 'Sorry, not a winning game.'

    def get_rows(self) -> List[list]:
        def _get_row(i):
            return [self.results[column][i] for column in range(self.num_columns)]

        return [_get_row(i) for i in range(self.num_columns)]

    def roll_reel(self, symbols):
        reel_size = self.num_columns + 2
        reel = []

        def add_to_reel(i):
            symbol = self._roll(symbols)
            if not is_previous_symbol(symbol, i):
                reel.append(symbol)
            else:
                add_to_reel(i)

        def is_previous_symbol(symbol, i):
            if len(reel) > 0:
                return symbol == reel[i - 1]

        [add_to_reel(i) for i in range(reel_size)]
        return reel

    def _add_result(self, column) -> None:
        self.results.append(column)

    def _roll_column(self) -> List[dict]:
        reel = self.roll_reel(self.reel)
        if len(self.results) > 0:
            reel += self.results[0]
            index = self._get_match_index(reel)
        else:
            index = 0
        column = []

        for i in range(self.num_columns):
            column.append(reel[index])
            index += 1
            if index > self.num_columns - 1:
                index = 0
        return column

    def _get_match_index(self, reel):
        first_column = self.results[0]
        symbol_to_match = first_column[self.bias_index]
        tilted_index = self._check_index_diagonals(self.bias_index)
        return reel.index(symbol_to_match) - tilted_index

    def _get_previous_column(self) -> List[dict]:
        previous = len(self.results) - 1
        if previous >= 0:
            return self.results[previous]

    def _check_index_diagonals(self, index):
        tilt = [index]
        if self._match_top_left_diagonal(index):
            top_left_diagonal = self._loop_reel(index - len(self.results))
            tilt.append(top_left_diagonal)
        if self._match_top_right_diagonal(index):
            top_right_diagonal = self._loop_reel(index + len(self.results))
            tilt.append(top_right_diagonal)
        return self._roll(tilt)

    def _loop_reel(self, index):
        if index > self.num_columns - 1:
            return index - (self.num_columns - 1)
        if index < 0:
            return self.num_columns + index
        return index

    def _match_top_left_diagonal(self, index) -> bool:
        return index == len(self.results)

    def _match_top_right_diagonal(self, index) -> bool:
        return len(self.results) == (self.num_columns - 1) - index

    @staticmethod
    def _roll(input_list: List) -> any:
        pick = random.randint(0, len(input_list) - 1)
        return input_list[pick]
