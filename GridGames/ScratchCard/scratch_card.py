from GridGames.ScratchCard.constants import *
from GridGames.grid_game_class import GridGame
from helper_functions import *
from joinable_game_class import JoinableGame


class ScratchCard(GridGame, JoinableGame):
    # Mechanics
    def __init__(self, host):
        GridGame.__init__(self)
        JoinableGame.__init__(self, host)
        self.max_time_left = 120
        self.num_columns = 3
        self.grid_size = self.num_columns * self.num_columns
        self.attempts_remaining = self.num_columns * 2
        self.card_grid = []
        self.underlying_symbols = []
        self.winnings = 0
        self.in_progress = True
        self.announcement = None
        self.card_render = None

    def initialize_card(self) -> None:
        random.shuffle(self.underlying_symbols)
        self._initialize_grids()

    def render_card(self) -> str:
        card = [CODE_TAG, self.card_render.render_card(), CODE_TAG]
        return LINEBREAK.join(card)

    def scratch_tiles(self, list_coordinates) -> None:
        for coordinates in list_coordinates:
            y = coordinates[0]
            x = coordinates[1]
            self._scratch(y, x)

    def _initialize_grids(self) -> None:
        self.underlying_symbols = self._generate_grid(self.underlying_symbols)
        neutral_tiles = [NEUTRAL_TILE] * self.grid_size
        self.card_grid = self._generate_grid(neutral_tiles)

    def _generate_grid(self, values: List) -> List[list]:
        # Creates a 2D array from a list (of length which should be a radical number)

        def get_next_value(i, j):
            next_index = i * self.num_columns + j
            return values[next_index]

        def create_row(i):
            return [get_next_value(i, j) for j in range(self.num_columns)]

        return [create_row(i) for i in range(self.num_columns)]

    def _scratch(self, y, x) -> None:
        self._reveal_tile(y, x)
        self.attempts_remaining -= 1

    def _reveal_tile(self, y, x):
        chosen_symbol = self._get_symbol(y, x)
        self.card_grid[y][x] = chosen_symbol

    def _get_symbol(self, y, x):
        return self.underlying_symbols[y][x]
