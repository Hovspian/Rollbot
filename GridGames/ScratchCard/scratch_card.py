from Core.helper_functions import *
from GridGames.ScratchCard.constants import *
from GridGames.grid import GridHandler
from Core.core_game_class import GameCore


class ScratchCard(GameCore):

    def __init__(self, ctx):
        super().__init__(ctx)
        self.max_time_left = 120
        self.num_columns = 3
        self.num_rows = 3
        self.payout = 0
        self.feedback = None  # TBD
        self.grid_handler = None  # TBD
        self.card_grid = None  # TBD
        self.grid_values = []  # TBD
        self.attempts_remaining = 3

    def initialize_card(self) -> None:
        random.shuffle(self.grid_values)
        self._initialize_grid()

    def scratch_tiles(self, list_coordinates) -> None:
        for coordinates in list_coordinates:
            y = coordinates[0]
            x = coordinates[1]
            self._scratch(y, x)

    def get_payout(self):
        return self.payout

    def _initialize_grid(self) -> None:
        self.grid_values = self.grid_handler.generate_grid(self.grid_values)
        self.grid_size = self.num_columns * self.num_columns
        neutral_tiles = [NEUTRAL_TILE] * self.grid_size
        self.card_grid = self.grid_handler.generate_grid(neutral_tiles)

    def _scratch(self, y, x) -> None:
        self._reveal_tile(y, x)
        self.attempts_remaining -= 1

    def _reveal_tile(self, y, x):
        self.card_grid[y][x] = self.grid_values[y][x]
