from GridGames.constants import *


class CoordinateParser:

    def __init__(self, grid_game):
        self.grid_game = grid_game
        self.attempts_remaining = grid_game.attempts_remaining
        self.num_columns = grid_game.num_columns

    @staticmethod
    def split_input(message):
        return message.split(',')

    def invalid_input(self, split_input):
        error = False
        valid_num_coordinates = 2
        if len(split_input) > self.attempts_remaining:
            error = 'Please make up to {} choices.'.format(self.attempts_remaining)
        for message in split_input:
            if len(message) != valid_num_coordinates:
                error = 'Please input the tile(s) you want to scratch. Eg: `/scratch A2`, `/scratch B1, C3`'
        return error

    def get_parse(self, message):
        split_input = self.split_input(message)
        return [self.add_valid_coordinates(input_coordinates) for input_coordinates in split_input]

    def add_valid_coordinates(self, input_coordinates):
        valid_parse = self.get_coordinates(input_coordinates)
        if valid_parse:
            return valid_parse

    def get_coordinates(self, input_coordinates):
        formatted_input = self.format_input_coordinates(input_coordinates)
        return self.parse_coordinates(formatted_input)

    @staticmethod
    def format_input_coordinates(input_coordinates):
        input_coordinates = input_coordinates.strip()
        return [coordinates.lower() for coordinates in input_coordinates]

    def parse_coordinates(self, input_coordinates):
        first_char = input_coordinates[0]
        second_char = input_coordinates[1]
        column_indexes = column_inputs[:self.num_columns]
        row_indexes = row_inputs[:self.num_columns]
        x = None
        y = None
        if first_char in column_indexes:
            y = column_indexes.index(first_char)
            if second_char in row_indexes:
                x = row_indexes.index(second_char)
        elif second_char in column_indexes:
            y = column_indexes.index(second_char)
            if first_char in row_indexes:
                x = row_indexes.index(first_char)
        if x is not None and y is not None:
            return [x, y]
        return False