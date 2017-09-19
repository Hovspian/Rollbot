from typing import List


class ResultChecker:
    def __init__(self, slot_machine):
        self.slot_machine = slot_machine
        self.get_rows = slot_machine.get_rows
        self.results = slot_machine.results
        self.winning_symbols = slot_machine.winning_symbols

    def analyze_results(self) -> None:
        self._check_rows()
        self._check_columns()
        self._check_top_left_diagonal()
        self._check_top_right_diagonal()

    def _check_columns(self):
        [self._check_winning_match(column) for column in self.results]

    def _check_rows(self):
        [self._check_winning_match(row) for row in self.get_rows()]

    def _check_top_left_diagonal(self) -> None:
        top_left_diagonal = self._get_diagonal(self.results)
        self._check_winning_match(top_left_diagonal)

    def _check_top_right_diagonal(self) -> None:
        reversed_columns = reversed(self.results)
        top_right_diagonal = self._get_diagonal(reversed_columns)
        self._check_winning_match(top_right_diagonal)

    @staticmethod
    def _get_diagonal(columns) -> List[dict]:
        return [column[i] for i, column in enumerate(columns)]

    def _check_winning_match(self, symbols: List[dict]) -> None:
        if self._is_all_matching(symbols):
            self._add_winning_match(symbols[0])

    @staticmethod
    def _is_all_matching(symbols) -> bool:
        for symbol in symbols:
            if symbol != symbols[0]:
                return False
        return True

    def _add_winning_match(self, symbol: dict) -> None:
        self.winning_symbols.append(symbol)


