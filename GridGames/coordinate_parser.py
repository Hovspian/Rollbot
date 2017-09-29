from GridGames.constants import *
from typing import List


class CoordinateParser:

    def __init__(self, num_columns):
        self.num_columns = num_columns

    @staticmethod
    def split_input(message) -> str:
        return message.split(',')

    def format_input(self, raw_input):
        input_coordinates = self.split_input(raw_input)

        def _format(coordinates):
            lower_case = coordinates.lower()
            removed_whitespace = lower_case.strip()
            return removed_whitespace

        return [_format(coordinates) for coordinates in input_coordinates]

    def get_parse(self, formatted_input) -> List[list]:
        valid_coordinates = [self._add_valid_coordinates(coordinates) for coordinates in formatted_input]
        if self._is_valid(valid_coordinates):
            return valid_coordinates

    def _add_valid_coordinates(self, coordinates) -> any:
        parsed = self._parse_coordinates(coordinates)
        if self._is_valid(parsed):
            return parsed

    @staticmethod
    def _is_valid(parse) -> bool:
        return None not in parse

    def _parse_coordinates(self, input_coordinates):
        x = None
        y = None
        column_indexes = column_inputs[:self.num_columns]
        row_indexes = row_inputs[:self.num_columns]
        for char in input_coordinates:
            if char in column_indexes:
                y = column_indexes.index(char)
            elif char in row_indexes:
                x = row_indexes.index(char)
        return [x, y]
