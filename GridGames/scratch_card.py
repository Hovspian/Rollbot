import random
import math
from typing import List
from GridGames.grid_game_class import GridGame
from GridGames.constants import *


class ScratchCard(GridGame):
    def __init__(self):
        super().__init__()
        self.num_winnable_combos = self.roll_num_winnable_combos()
        self.symbols = []
        self.grid_size = self.num_columns * self.num_columns
        self.chances_remaining = 6
        self.matches_to_win = self.chances_remaining // 2
        self.card_grid = [neutral_tile] * self.grid_size
        self.winning_symbols = []
        self.in_progress = True
        self.default_values = [empty,
                               empty,
                               empty,
                               one,
                               one,
                               three,
                               three,
                               five,
                               five,
                               ten,
                               ten,
                               hundred]

    def initialize_card(self):
        self.add_winnable_value()
        self.add_random_values()
        random.shuffle(self.symbols)
        print(self.symbols)
        self.initialize_rows()

    def initialize_rows(self):
        self.symbols = self.generate_rows(self.symbols)
        for row in self.symbols:
            print(row)
        self.card_grid = self.generate_rows(self.card_grid)

    def roll_num_winnable_combos(self):
        combos = [1, 1, 2]
        return self._roll(combos)

    def add_winnable_value(self):
        for i in range(self.num_winnable_combos):
            self.symbols += self.roll_winnable_value()

    def roll_winnable_value(self):
        winnable_symbols = self.remove_symbol(self.default_values, empty)
        symbol = self._roll(winnable_symbols)
        return [symbol] * self.matches_to_win

    def add_random_values(self):
        symbols_remaining = self.grid_size - len(self.symbols)
        for i in range(symbols_remaining):
            symbol = self._roll(self.default_values)
            self.symbols.append(symbol)

    def generate_columns(self, symbols):
        def create_column(i):
            return [symbols[i*self.num_columns + j] for j in range(self.num_columns)]
        return [create_column(i) for i in range(self.num_columns)]

    def generate_rows(self, symbols):
        # TODO skip column generation
        columns = self.generate_columns(symbols)
        return self.get_rows(columns)

    def draw_card(self):
        horizontal_header = space.join([corner] + horizontal_labels[:self.num_columns])
        tiles = []
        for i, row in enumerate(self.card_grid):
            row_emotes = ''.join(self.get_emotes(row))
            tiles.append(vertical_labels[i] + row_emotes)
        tile_string = '\n'.join(tiles)
        return '\n'.join([horizontal_header, tile_string])

    def parse_input(self, message):
        split_input = self.split_input(message)
        scratch_tiles = []
        for input_coordinates in split_input:
            parsed = self.parse_coordinates(input_coordinates)
            if parsed:
                scratch_tiles.append(parsed)
        return scratch_tiles

    def parse_coordinates(self, input_coordinates):
        input_coordinates = input_coordinates.strip()
        coordinates = self.get_coordinates(input_coordinates)
        return coordinates

    def get_coordinates(self, input_coordinates):
        first_char = input_coordinates[0].lower()
        second_char = input_coordinates[1].lower()
        horizontal = horizontal_inputs[:self.num_columns]
        vertical = vertical_inputs[:self.num_columns]
        x = None
        y = None
        if first_char in horizontal:
            x = horizontal.index(first_char)
            if second_char in vertical:
                y = vertical.index(second_char)
        elif second_char in horizontal:
            x = horizontal.index(second_char)
            if first_char in vertical:
                y = vertical.index(first_char)
        if x is not None and y is not None:
            return [x, y]
        return False

    def scratch_tiles(self, tiles):
        # TODO report tiles which have already been scratched
        for tile in tiles:
            x = tile[0]
            y = tile[1]
            if self.card_grid[x][y] is neutral_tile:
                chosen_symbol = self.symbols[x][y]
                self.card_grid[x][y] = chosen_symbol
                self.check_winning_symbol(chosen_symbol)
                self.chances_remaining -= 1
        self.check_game_end()

    def check_winning_symbol(self, symbol):
        if symbol is not empty:
            self.results.append(symbol)

    def invalid_input(self, split_input):
        error = False
        if len(split_input) > self.chances_remaining:
            error = 'Please make up to {} choices.'.format(self.chances_remaining)
        for message in split_input:
            if len(message) != 2:
                error = 'Please input the tile(s) you want to scratch. Eg: `/scratch A2`, `/scratch B1, C3`'
        return error

    def check_game_end(self):
        if self.chances_remaining <= 0:
            self.check_results()
            self.in_progress = False

    def check_results(self):
        results = self.results
        def match_counter(results):
            i = 0
            for result in results:
                if result == results[0]:
                    i += 1
                    print("Num of winners", i)
            if i >= self.matches_to_win:
                self.winning_symbols.append(results[0])
        while len(results) > 0:
            print("results", results)
            match_counter(results)
            results = self.remove_symbol(results, results[0])

    def get_report(self):
        if len(self.winning_symbols) >= 1:
            return '\n'.join(["Winning match!", self.get_winning_report()])
        else:
            return 'Sorry, not a winning game.'

    def get_winning_report(self):
        payout_stats = '\n'.join([self._symbol_stats(match) for match in self.winning_symbols])
        payout = self.calculate_payout()
        payout_message = ':dollar: Payout is {} gold. :dollar:'.format(payout)
        return '\n'.join([payout_stats, payout_message])

    @staticmethod
    def _symbol_stats(symbol):
        return ': '.join([str(symbol[key]) for key in symbol])
