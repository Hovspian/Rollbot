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

    def play_slot(self) -> None:
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

    @staticmethod
    def get_lose_message() -> str:
        return 'Sorry, not a winning game.'

    def get_rows(self) -> List[list]:
        def _get_row(i):
            return [self.results[column][i] for column in range(self.num_columns)]
        return [_get_row(i) for i in range(self.num_columns)]

    def _add_result(self, column) -> None:
        self.results.append(column)

    def _roll_column(self) -> List[dict]:
        symbol_container = [self._roll_container(current_index) for current_index in range(self.num_columns)]
        return [self._roll(symbols) for symbols in symbol_container]

    def _roll_container(self, current_index) -> List[dict]:
        containers = self._get_containers(current_index)
        picked_container = self._roll(containers)
        return picked_container

    def _get_containers(self, current_index):
        containers = self._get_default_containers()
        previous_column = self._get_previous_column()
        if previous_column:
            biased_containers = self._get_biased_containers(current_index)
            containers += biased_containers
        return containers

    def _get_default_containers(self) -> List[list]:
        return [self.default_outcomes, self.default_outcomes, self.default_outcomes]

    def _get_biased_containers(self, current_index) -> List[list]:
        previous_column = self._get_previous_column()
        previous_symbol = [previous_column[current_index]]
        first_column = self.results[0]
        containers = [first_column, first_column, previous_symbol]
        previous_diagonals = self._get_previous_diagonals(current_index)
        for diagonal in previous_diagonals:
            containers.append([diagonal])
        return containers

    def _get_previous_diagonals(self, current_index) -> List[dict]:
        previous_column = self._get_previous_column()
        diagonals = []
        if self._match_top_left_diagonal(current_index):
            upper_left = current_index - 1
            diagonals.append(previous_column[upper_left])
        if self._match_top_right_diagonal(current_index):
            lower_left = current_index + 1
            diagonals.append(previous_column[lower_left])
        return diagonals

    def _match_top_left_diagonal(self, current_index) -> bool:
        return current_index == len(self.results)

    def _match_top_right_diagonal(self, current_index) -> bool:
        return len(self.results) == (self.num_columns - 1) - current_index

    def _get_previous_column(self) -> List[dict]:
        previous = len(self.results) - 1
        if previous >= 0:
            return self.results[previous]

    @staticmethod
    def _roll(input_list: List) -> any:
        pick = random.randint(0, len(input_list) - 1)
        return input_list[pick]