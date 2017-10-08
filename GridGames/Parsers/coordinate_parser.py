from typing import List
from GridGames.ScratchCard.constants import *


class CoordinateParser:

    def __init__(self):
        pass

    @staticmethod
    def split_input(message) -> str:
        return message.split(',')

    def format_input(self, raw_input):
        input_coordinates = self.split_input(raw_input)
        return [self._format(coordinates) for coordinates in input_coordinates]

    @staticmethod
    def _format(coordinates):
        lower_case = coordinates.lower()
        removed_whitespace = lower_case.strip()
        return removed_whitespace

    def get_parse(self, formatted_input) -> List[list]:
        return [self._add_valid_coordinates(coordinates) for coordinates in formatted_input]

    def _add_valid_coordinates(self, coordinates) -> any:
        parsed = self._parse_coordinates(coordinates)
        if self._is_valid(parsed):
            return parsed

    @staticmethod
    def _is_valid(parse) -> bool:
        return None not in parse

    @staticmethod
    def _parse_coordinates(input_coordinates):
        y = None
        x = None
        column_indexes = COLUMN_INPUTS
        row_indexes = ROW_INPUTS
        for char in input_coordinates:
            if char in column_indexes:
                x = column_indexes.index(char)
            elif char in row_indexes:
                y = row_indexes.index(char)
        return [y, x]
