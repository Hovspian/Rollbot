import random
from typing import List
from GridGames.ScratchCard.constants import *
from GridGames.ScratchCard.scratch_card_feedback import ScratchCardFeedback
from GridGames.grid_game_class import GridGame


class ScratchCard(GridGame):
    # Mechanics
    def __init__(self):
        super().__init__()
        self.num_winnable_combos = self._roll_num_winnable_combos()
        self.num_columns = 3
        self.grid_size = self.num_columns * self.num_columns
        self.attempts_remaining = self.num_columns * 2
        self.matches_to_win = self.attempts_remaining // 2
        self.card_grid = []
        self.underlying_symbols = []
        self.winning_symbols = []
        self.in_progress = True
        self.default_values = [EMPTY_TILE,
                               EMPTY_TILE,
                               EMPTY_TILE,
                               ONE,
                               ONE,
                               THREE,
                               THREE,
                               FIVE,
                               FIVE,
                               TEN,
                               TEN,
                               HUNDRED]
        self.announcement = ScratchCardFeedback(self)
        self.initialize_card()

    def initialize_card(self) -> None:
        self._add_winnable_combo()
        self._add_random_values()
        random.shuffle(self.underlying_symbols)
        self._initialize_grids()

    def scratch_tiles(self, list_coordinates) -> None:
        for coordinates in list_coordinates:
            y = coordinates[0]
            x = coordinates[1]
            self._scratch(y, x)
        self._check_game_end()

    def render_card(self) -> str:
        column_header = SPACE.join([CORNER] + COLUMN_LABELS[:self.num_columns])
        tiles = []
        for i, row in enumerate(self.card_grid):
            row_emotes = ''.join(self.get_emotes(row))
            tiles.append(ROW_LABELS[i] + row_emotes)
        tile_string = '\n'.join(tiles)
        return '\n'.join([column_header, tile_string])

    def _initialize_grids(self) -> None:
        self.underlying_symbols = self._generate_grid(self.underlying_symbols)
        neutral_tiles = [NEUTRAL_TILE] * self.grid_size
        self.card_grid = self._generate_grid(neutral_tiles)

    def _roll_num_winnable_combos(self) -> int:
        combos = [1, 1, 2]
        return self._roll(combos)

    def _add_winnable_combo(self) -> None:
        for i in range(self.num_winnable_combos):
            self.underlying_symbols += self._roll_winnable_value()

    def _roll_winnable_value(self) -> List[dict]:
        winnable_symbols = self.remove_value_from(container=self.default_values, filter_value=EMPTY_TILE)
        symbol = self._roll(winnable_symbols)
        return [symbol] * self.matches_to_win

    def _add_random_values(self) -> None:
        symbols_remaining = self.grid_size - len(self.underlying_symbols)
        for i in range(symbols_remaining):
            symbol = self._roll(self.default_values)
            self.underlying_symbols.append(symbol)

    def _generate_grid(self, values: List) -> List[list]:
        def create_line(i):
            return [values[i * self.num_columns + j] for j in range(self.num_columns)]

        return [create_line(i) for i in range(self.num_columns)]

    def _scratch(self, y, x) -> None:
        chosen_symbol = self.underlying_symbols[y][x]
        self.card_grid[y][x] = chosen_symbol
        self._check_winnable_symbol(chosen_symbol)
        self.attempts_remaining -= 1

    def _check_winnable_symbol(self, symbol) -> None:
        if symbol is not EMPTY_TILE:
            self.results.append(symbol)

    def _check_game_end(self) -> None:
        if self.attempts_remaining <= 0:
            self._check_results()
            self.in_progress = False

    def _check_results(self) -> None:
        results = self.results

        def count_match():
            i = 0
            for result in results:
                if result == results[0]:
                    i += 1
                    add_if_match(i)

        def add_if_match(i):
            if i >= self.matches_to_win:
                self.winning_symbols.append(results[0])

        while len(results) > 0:
            count_match()
            results = self.remove_value_from(results, results[0])


