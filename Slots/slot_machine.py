import random
from typing import List
from Slots.result_checker import ResultChecker
from Slots.slots_feedback import SlotsFeedback

BIAS_TYPE = {'row': 0, 'diagonal': 1}


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
        self.bias_type = 0

    def play_slot(self) -> None:
        self.reel = self.roll_reel(self.default_outcomes)
        self._roll_bias_index()
        self._determine_bias_type()

        def _perform_rolls():
            self._add_result(self._roll_column())

        [_perform_rolls() for i in range(self.num_columns)]
        ResultChecker(self).analyze_results()

    def _roll_bias_index(self):
        first_row = 0
        last_row = self.num_columns - 1
        random_index = random.randint(first_row, last_row)
        self.bias_index = self._roll([first_row, last_row, random_index])

    def _determine_bias_type(self):
        bias_is_first_row = self.bias_index == 0
        bias_is_last_row = self.bias_index == self.num_columns - 1
        if bias_is_first_row or bias_is_last_row:
            self.bias_type = self._roll([BIAS_TYPE['row'], BIAS_TYPE['diagonal'], BIAS_TYPE['diagonal']])

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
        if self.bias_type == BIAS_TYPE['diagonal']:
            bias_index = self._check_index_diagonals()
        else:
            bias_index = self.bias_index
        return reel.index(symbol_to_match) - bias_index

    def _get_previous_column(self) -> List[dict]:
        previous = len(self.results) - 1
        if previous >= 0:
            return self.results[previous]

    def _check_index_diagonals(self):
        if self.bias_index == 0:
            top_left_diagonal = self._loop_reel(self.bias_index + len(self.results))
            return top_left_diagonal
        if self.bias_index == self.num_columns - 1:
            top_right_diagonal = self._loop_reel(self.bias_index - len(self.results))
            return top_right_diagonal
        return self.bias_index

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
