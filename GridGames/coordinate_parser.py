from GridGames.constants import *
from typing import List


class CoordinateParser:

    def __init__(self, grid_game):
        self.grid_game = grid_game
        self.attempts_remaining = grid_game.attempts_remaining
        self.num_columns = grid_game.num_columns

    @staticmethod
    def split_input(message) -> str:
        return message.split(',')

    def check_invalid_input(self, split_input) -> any:
        error = False
        valid_num_coordinates = 2
        if len(split_input) > self.attempts_remaining:
            error = 'Please make up to {} choices.'.format(self.attempts_remaining)
        for message in split_input:
            if len(message) != valid_num_coordinates:
                error = 'Please input the tile(s) you want to scratch. Eg: `/scratch A2`, `/scratch B1, C3`'
        return error

    def get_parse(self, message) -> List[list]:
        split_input = self.split_input(message)
        return [self.add_valid_coordinates(input_coordinates) for input_coordinates in split_input]

    def add_valid_coordinates(self, input_coordinates) -> any:
        formatted_input = self.format_input_coordinates(input_coordinates)
        parse = self.parse_coordinates(formatted_input)
        if self.is_valid_parse(parse):
            return parse

    @staticmethod
    def is_valid_parse(parse) -> bool:
        return None not in parse

    @staticmethod
    def format_input_coordinates(input_coordinates):
        input_coordinates = input_coordinates.strip()
        return [coordinates.lower() for coordinates in input_coordinates]

    def parse_coordinates(self, input_coordinates):
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