import random
import math
from typing import List
from GridGames.grid_game_class import GridGame
from GridGames.constants import *
from GridGames.coordinate_parser import CoordinateParser


class ScratchCard(GridGame):

    def __init__(self, host):
        super().__init__(host)
        self.num_winnable_combos = self.roll_num_winnable_combos()
        self.num_columns = 3
        self.grid_size = self.num_columns * self.num_columns
        self.attempts_remaining = self.num_columns * 2
        self.matches_to_win = self.attempts_remaining // 2
        self.card_grid = [neutral_tile] * self.grid_size
        self.card_symbols = []
        self.winning_symbols = []
        self.in_progress = True
        self.input_parser = CoordinateParser(self)
        self.default_values = [empty_tile,
                               empty_tile,
                               empty_tile,
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
        self.add_winnable_combo()
        self.add_random_values()
        random.shuffle(self.card_symbols)
        self.initialize_rows()

    def initialize_rows(self):
        self.card_symbols = self.generate_rows(self.card_symbols)
        self.card_grid = self.generate_rows(self.card_grid)

    def roll_num_winnable_combos(self):
        combos = [1, 1, 2]
        return self._roll(combos)

    def get_starting_message(self):
        return '\n'.join(['New scratch card for {}.'.format(self.host_name),
                          self._render_card(),
                          'Match {} symbols to win!'.format(self.matches_to_win),
                          'You have {} attempts remaining.'.format(self.attempts_remaining)])

    def add_winnable_combo(self):
        for i in range(self.num_winnable_combos):
            self.card_symbols += self.roll_winnable_value()

    def roll_winnable_value(self):
        winnable_symbols = self.remove_value_from(container=self.default_values, filter_value=empty_tile)
        symbol = self._roll(winnable_symbols)
        return [symbol] * self.matches_to_win

    def parse_input(self, input):
        return self.input_parser.get_parse(input)

    def add_random_values(self):
        symbols_remaining = self.grid_size - len(self.card_symbols)
        for i in range(symbols_remaining):
            symbol = self._roll(self.default_values)
            self.card_symbols.append(symbol)

    def generate_rows(self, symbols):
        def create_column(i):
            return [symbols[i * self.num_columns + j] for j in range(self.num_columns)]
        return [create_column(i) for i in range(self.num_columns)]

    def get_card_state(self):
        return '\n'.join(["{}'s scratch card".format(self.host_name),
                          self._render_card()])

    def _render_card(self):
        column_header = space.join([corner] + column_labels[:self.num_columns])
        tiles = []
        for i, row in enumerate(self.card_grid):
            row_emotes = ''.join(self.get_emotes(row))
            tiles.append(row_labels[i] + row_emotes)
        tile_string = '\n'.join(tiles)
        return '\n'.join([column_header, tile_string])

    def scratch_tiles(self, list_coordinates):
        # TODO report tiles which have already been scratched
        for coordinates in list_coordinates:
            x = coordinates[0]
            y = coordinates[1]
            tile = self.card_grid[x][y]
            if self.is_scratchable(tile):
                self.scratch(x, y)
        self.check_game_end()

    @staticmethod
    def is_scratchable(tile) -> bool:
        return tile is neutral_tile

    def scratch(self, x, y):
        chosen_symbol = self.card_symbols[x][y]
        self.card_grid[x][y] = chosen_symbol
        self.check_winnable_symbol(chosen_symbol)
        self.attempts_remaining -= 1

    def check_winnable_symbol(self, symbol):
        if symbol is not empty_tile:
            self.results.append(symbol)

    def check_game_end(self):
        if self.attempts_remaining <= 0:
            self.check_results()
            self.in_progress = False

    def check_results(self):
        results = self.results

        def match_counter():
            i = 0
            for result in results:
                if result == results[0]:
                    i += 1
            if i >= self.matches_to_win:
                self.winning_symbols.append(results[0])

        while len(results) > 0:
            match_counter()
            results = self.remove_value_from(results, results[0])

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
