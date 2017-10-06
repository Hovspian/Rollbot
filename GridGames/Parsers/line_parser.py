from GridGames.Parsers.coordinate_parser import CoordinateParser
from GridGames.ScratchCard.constants import *


class LineParser(CoordinateParser):
    # A CoordinateParser which can also return a line of tiles (column, row or diagonal) based on user input
    def __init__(self, num_columns):
        super().__init__(num_columns)
        self.num_columns = num_columns
        self.column_inputs = COLUMN_INPUTS[:self.num_columns]
        self.row_inputs = ROW_INPUTS[:self.num_columns]

    def get_line(self, raw_input):
        # Eg. a = [ [0][0], [0][1], [0][2] ]
        formatted_input = self._format(raw_input)
        diagonal = self.check_diagonal(formatted_input)
        column = self.check_column(formatted_input)
        row = self.check_row(formatted_input)

        return diagonal or column or row or None

    def check_column(self, first_character):
        column = []
        if first_character in self.column_inputs:
            x = self.column_inputs.index(first_character)
            for y in range(self.num_columns):
                column.append([y, x])
        return column

    def check_row(self, first_character):
        row = []
        if first_character in self.row_inputs:
            y = self.row_inputs.index(first_character)
            for x in range(self.num_columns):
                row.append([y, x])
        return row

    def check_diagonal(self, formatted_input):
        split_input = self.split_input(formatted_input)
        parse = self.get_parse(split_input)
        if parse and len(formatted_input) == 2:
            coordinates = parse[0]
            return self.get_diagonal(coordinates)

    def get_diagonal(self, parse):
        # Returns the proper diagonal based on the sum of the parsed coordinates
        start = 0
        last_of_row_or_column = self.num_columns - 1
        sum_value = sum(parse)
        if sum_value == start:
            return self.get_left_diagonal_coordinates()
        elif sum_value == last_of_row_or_column:
            return self.get_right_diagonal_coordinates()

    def get_left_diagonal_coordinates(self):
        line = []
        for i in range(self.num_columns):
            line.append([i, i])
        return line

    def get_right_diagonal_coordinates(self):
        line = []
        for i in range(self.num_columns):
            row = (self.num_columns - 1) - i
            line.append([row, i])
        return line
