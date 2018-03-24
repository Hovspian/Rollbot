from typing import List

from Slots.symbols import DITTO


class ResultChecker:
    def __init__(self, slot_machine):
        self.slot_machine = slot_machine
        self.results = slot_machine.results
        self.winning_symbols = slot_machine.winning_symbols
        self.winning_combos = slot_machine.winning_combos

    def analyze_results(self) -> None:
        self._check_rows()
        self._check_top_left_diagonal()
        self._check_top_right_diagonal()

    def _check_rows(self):
        [self._check_combo(row, combo_name='row') for row in self._get_rows(self.results)]

    def _check_top_left_diagonal(self) -> None:
        top_left_diagonal = self._get_diagonal(self.results)
        self._check_combo(top_left_diagonal, combo_name='diagonal')

    def _check_top_right_diagonal(self) -> None:
        reversed_columns = reversed(self.results)
        top_right_diagonal = self._get_diagonal(reversed_columns)
        self._check_combo(top_right_diagonal, combo_name='diagonal')

    @staticmethod
    def _get_rows(grid):

        def _get_row(i):
            return [grid[column][i] for column, item in enumerate(grid)]

        return [_get_row(i) for i, item in enumerate(grid)]

    @staticmethod
    def _get_diagonal(columns) -> List[dict]:
        return [column[i] for i, column in enumerate(columns)]

    def _check_combo(self, symbols: List[dict], combo_name):
        if self._check_winning_match(symbols):
            self._add_winning_combo(combo_name)

    def _check_winning_match(self, symbols: List[dict]) -> bool:
        if self._is_all_matching(symbols):
            self._add_winning_match(symbols[0])
            return True

    @staticmethod
    def _is_all_matching(symbols: List[dict]) -> bool:
        return all(symbol == symbols[0] or symbol == DITTO for symbol in symbols)

    def _add_winning_combo(self, combo_name: str) -> None:
        self.winning_combos.append(combo_name)

    def _add_winning_match(self, symbol: dict) -> None:
        self.winning_symbols.append(symbol)