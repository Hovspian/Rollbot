from typing import List


class GridHandler:
    def __init__(self, num_columns=3, num_rows=3):
        self.num_rows = num_rows
        self.num_columns = num_columns
        self.columns = []

    def get_grid(self) -> List[list]:
        return self.columns

    def generate_grid(self, values: List) -> List[list]:
        # Creates a 2D array from a list

        def get_next_value(i, j):
            next_index = i * self.num_columns + j
            return values[next_index]

        def create_row(i):
            return [get_next_value(i, j) for j in range(self.num_columns)]

        return [create_row(i) for i in range(self.num_rows)]

    def get_rows(self) -> List[list]:
        num_columns = len(self.columns)

        def _get_row(i):
            return [self.columns[column][i] for column in range(num_columns)]
        return [_get_row(i) for i in range(num_columns)]

    def add_column(self, column):
        self.columns.append(column)

    def get_emotes(self, symbols) -> str:
        return ''.join(self.get_emote_list(symbols))

    def get_emote_list(self, symbols):
        return [self.get_emote(symbol) for symbol in symbols]

    def get_top_left_diagonal(self, column_grid) -> List[dict]:
        return self._get_diagonal(column_grid)

    def get_top_right_diagonal(self, column_grid) -> List[dict]:
        reversed_columns = reversed(column_grid)
        return self._get_diagonal(reversed_columns)

    @staticmethod
    def get_emote(symbol):
        return symbol['emote']

    @staticmethod
    def get_value(symbol):
        return symbol['value']

    @staticmethod
    def _get_diagonal(column_grid) -> List[dict]:
        return [column[i] for i, column in enumerate(column_grid)]