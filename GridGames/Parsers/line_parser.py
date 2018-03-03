from GridGames.Parsers.coordinate_parser import CoordinateParser
from GridGames.ScratchCard.constants import *
from typing import List


class LineParser(CoordinateParser):
    # Returns a line of tiles (column, row or diagonal) based on user input and game board size
    def __init__(self):
        super().__init__()

    def get_line(self, game, raw_input) -> List[List[int]]:
        # Eg. 'a' outputs [ [0][0], [0][1], [0][2] ]
        num_columns = game.num_columns
        formatted_input = self._format(raw_input)

        if formatted_input in COLUMN_INPUTS:
            return self.get_column(formatted_input, num_columns)

        if formatted_input in ROW_INPUTS:
            return self.get_row(formatted_input, num_columns)

        diagonal = self.check_diagonal(formatted_input, num_columns)
        if diagonal:
            return diagonal

    def check_diagonal(self, formatted_input, num_columns) -> List[List[int]]:
        parse = self._parse_coordinates(formatted_input)
        if parse:
            return self.get_diagonal(parse, num_columns)

    def get_diagonal(self,  parse, num_columns) -> List[List[int]]:
        # Returns a diagonal based on the sum of the parsed coordinates
        sum_value = sum(parse)
        start = 0
        last_of_row_or_column = num_columns - 1
        if sum_value == start:
            return self.get_left_diagonal(num_columns)
        elif sum_value == last_of_row_or_column:
            return self.get_right_diagonal(num_columns)

    @staticmethod
    def get_column(formatted_input, num_columns) -> List[List[int]]:
        x = COLUMN_INPUTS.index(formatted_input)
        return [[y, x] for y in range(num_columns)]

    @staticmethod
    def get_row(formatted_input, num_columns) -> List[List[int]]:
        y = ROW_INPUTS.index(formatted_input)
        return [[y, x] for x in range(num_columns)]

    @staticmethod
    def get_left_diagonal(num_columns) -> List[List[int]]:
        return [[i, i] for i in range(num_columns)]

    @staticmethod
    def get_right_diagonal(num_columns) -> List[List[int]]:

        def get_coordinates(i):
            row = (num_columns - 1) - i
            return [row, i]

        return [get_coordinates(i) for i in range(num_columns)]
