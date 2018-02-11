from Core.helper_functions import *
from GridGames.ScratchCard.constants import *
from GridGames.grid import GridHandler
from Core.core_game_class import GameCore


class ScratchCard(GameCore):
    # Mechanics
    def __init__(self, ctx):
        super().__init__(ctx)
        self.max_time_left = 120
        self.num_columns = 3
        self.attempts_remaining = self.num_columns * 2
        self.payout = 0
        self.feedback = None  # TBD
        self.card_renderer = None  # TBD
        self.grid_handler = None  # TBD
        self.card_grid = None  # TBD
        self.underlying_symbols = []  # TBD
        self.title = "Scratch Card"
        self.start_game()

    def initialize_card(self) -> None:
        random.shuffle(self.underlying_symbols)
        self._initialize_grids()

    def render_card(self) -> str:
        card = [CODE_TAG, self.card_renderer.render_card(), CODE_TAG]
        return LINEBREAK.join(card)

    def scratch_tiles(self, list_coordinates) -> None:
        for coordinates in list_coordinates:
            y = coordinates[0]
            x = coordinates[1]
            self._scratch(y, x)

    def get_payout(self):
        return self.payout

    def _initialize_grids(self) -> None:
        self.underlying_symbols = self.grid_handler.generate_grid(self.underlying_symbols)
        self.grid_size = self.num_columns * self.num_columns
        neutral_tiles = [NEUTRAL_TILE] * self.grid_size
        self.card_grid = self.grid_handler.generate_grid(neutral_tiles)

    def _scratch(self, y, x) -> None:
        self._reveal_tile(y, x)
        self.attempts_remaining -= 1

    def _reveal_tile(self, y, x):
        self.card_grid[y][x] = self.underlying_symbols[y][x]
