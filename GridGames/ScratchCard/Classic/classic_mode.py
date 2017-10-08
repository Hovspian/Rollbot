from GridGames.ScratchCard.Classic.feedback import ScratchCardFeedback
from GridGames.ScratchCard.constants import *
from GridGames.ScratchCard.scratch_card import ScratchCard
from GridGames.helper_functions import *
from GridGames.render_card import RenderCard


class ClassicScratchCard(ScratchCard):
    def __init__(self):
        super().__init__()
        self.num_winnable_combos = self._roll_num_winnable_combos()
        self.matches_to_win = self.attempts_remaining // 2
        self.winning_symbols = []
        self.announcement = ScratchCardFeedback(self)
        self.default_values = [EMPTY_TILE,
                               FIVE,
                               FIVE,
                               TEN,
                               TEN,
                               TWENTY_FIVE,
                               TWENTY_FIVE,
                               FIFTY,
                               FIFTY,
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
