from typing import List
from GridGames.ScratchCard.constants import *


class CoordinateParser:

    """
    Turns a string such as "A2, B0, C1" into [[2, 0], [0, 1], [1, 3]].
    "A2, B0, C1" -> ["a2", "b0", "c1"] -> [[2, 0], [0, 1], [1, 3]]
    """

    @staticmethod
    def split_input(message) -> str:
        return message.split(',')

    def format_input(self, raw_input) -> List[str]:
        # Eg. returns ["a2", "b0", "c1"]
        input_coordinates = self.split_input(raw_input)
        return [self._format(coordinates) for coordinates in input_coordinates]

    def get_single_parse(self, formatted_input: List[str]):
        # Ignore all entries except the first one.
        coordinates = formatted_input[0]
        validated = self._parse_coordinates(coordinates)
        if validated:
            return validated

    def get_parse(self, formatted_input: List[str]) -> List[list]:
        # Eg. returns [[0, 1], [2, 0]]
        valid_coordinates = []
        for coordinates in formatted_input:
            validated = self._parse_coordinates(coordinates)
            if validated:
                valid_coordinates.append(validated)
        return valid_coordinates

    @staticmethod
    def _format(coordinates):
        # Eg. "  A2" -> "a2"
        lower_case = coordinates.lower()
        removed_whitespace = lower_case.strip()
        return removed_whitespace

    @staticmethod
    def _parse_coordinates(input_coordinates) -> List[int] or None:
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
