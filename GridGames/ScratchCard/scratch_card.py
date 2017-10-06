from GridGames.ScratchCard.constants import *
from GridGames.ScratchCard.feedback import ScratchCardFeedback
from GridGames.grid_game_class import GridGame
from GridGames.helper_functions import *
from GridGames.render_card import RenderCard


class ScratchCard(GridGame):
    # Mechanics
    def __init__(self):
        super().__init__()
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
        self._initialize_grids()
        random.shuffle(self.underlying_symbols)

    def scratch_tiles(self, list_coordinates) -> None:
        for coordinates in list_coordinates:
            y = coordinates[0]
            x = coordinates[1]
            self._scratch(y, x)

    def render_card(self) -> str:
        card = [CODE_TAG, self.card_render.render_card(), CODE_TAG]
        return LINEBREAK.join(card)

    def _initialize_grids(self) -> None:
        self.underlying_symbols = self._generate_grid(self.underlying_symbols)
        neutral_tiles = [NEUTRAL_TILE] * self.grid_size
        self.card_grid = self._generate_grid(neutral_tiles)

    def _generate_grid(self, values: List) -> List[list]:
        def create_line(i):
            return [values[i * self.num_columns + j] for j in range(self.num_columns)]

        return [create_line(i) for i in range(self.num_columns)]

    def _scratch(self, y, x) -> None:
        self._reveal_tile(y, x)
        self.attempts_remaining -= 1

    def _reveal_tile(self, y, x):
        chosen_symbol = self._get_symbol(y, x)
        self.card_grid[y][x] = chosen_symbol

    def _get_symbol(self, y, x):
        return self.underlying_symbols[y][x]


class ClassicScratchCard(ScratchCard):
    def __init__(self):
        super().__init__()
        self.num_winnable_combos = self._roll_num_winnable_combos()
        self.matches_to_win = self.attempts_remaining // 2
        self.winning_symbols = []
        self.announcement = ScratchCardFeedback(self)
        self.default_values = [EMPTY_TILE,
                               EMPTY_TILE,
                               FIVE,
                               FIVE,
                               FIVE,
                               TEN,
                               TEN,
                               TEN,
                               TEN,
                               TWENTY_FIVE,
                               TWENTY_FIVE,
                               FIFTY,
                               FIFTY,
                               HUNDRED,
                               HUNDRED]

    @staticmethod
    def _roll_num_winnable_combos() -> int:
        combos = [1, 2]
        return roll(combos)

    def initialize_card(self):
        self._add_winnable_combo()
        self._add_random_values()
        super().initialize_card()
        self.card_render = RenderCard(self)

    def _add_winnable_combo(self) -> None:
        for i in range(self.num_winnable_combos):
            self.underlying_symbols += self._roll_winnable_value()

    def _roll_winnable_value(self) -> List[dict]:
        winnable_symbols = remove_value(container=self.default_values, filter_value=EMPTY_TILE)
        symbol = roll(winnable_symbols)
        return [symbol] * self.matches_to_win

    def _add_random_values(self) -> None:
        symbols_remaining = self.grid_size - len(self.underlying_symbols)
        for i in range(symbols_remaining):
            symbol = roll(self.default_values)
            self.underlying_symbols.append(symbol)

    def scratch_tiles(self, list_coordinates):
        super().scratch_tiles(list_coordinates)
        self._check_game_end()

    def _check_game_end(self) -> None:
        if self.attempts_remaining <= 0:
            self._check_results()
            self.in_progress = False

    def _scratch(self, y, x):
        super()._scratch(y, x)
        chosen_symbol = self.underlying_symbols[y][x]
        self._check_winnable_symbol(chosen_symbol)

    def _check_winnable_symbol(self, symbol) -> None:
        if symbol is not EMPTY_TILE:
            self.results.append(symbol)

    def _check_results(self) -> None:
        results = self.results

        def count_match() -> None:
            i = 0
            for result in results:
                if result == results[0]:
                    i += 1
            add_if_match(i)

        def add_if_match(i):
            if i >= self.matches_to_win:
                self.winning_symbols.append(results[0])

        while results:
            count_match()
            results = remove_value(results, results[0])