from Core.constants import GAME_ID
from Core.helper_functions import *
from GridGames.ScratchCard.Classic.feedback import ScratchCardFeedback
from GridGames.ScratchCard.constants import *
from GridGames.ScratchCard.scratch_card import ScratchCard
from GridGames.grid import GridHandler
from GridGames.grid_renderer import CardRenderer
import math


class ClassicScratchCard(ScratchCard):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.num_winnable_combos = self._roll_num_winnable_combos()
        self.attempts_remaining = self.num_columns * 2
        self.matches_to_win = self.attempts_remaining // 2
        self.winning_symbols = []
        self.results = []
        self.feedback = ScratchCardFeedback(self)
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
        self.grid_handler = GridHandler(num_columns=self.num_columns, num_rows=self.num_columns)
        self.id = GAME_ID["SCRATCHCARD"]
        self.initialize_card()

    @staticmethod
    def _roll_num_winnable_combos() -> int:
        combos = [1, 2]
        return roll(combos)

    def initialize_card(self):
        self.start_game()
        self._add_winnable_combo()
        self._add_random_values()
        super().initialize_card()

    def _add_winnable_combo(self) -> None:
        for i in range(self.num_winnable_combos):
            self.grid_values += self._roll_winnable_value()

    def _roll_winnable_value(self) -> List[dict]:
        winnable_symbols = filter_value(container=self.default_values, value_to_filter=EMPTY_TILE)
        symbol = roll(winnable_symbols)
        return [symbol] * self.matches_to_win

    def _add_random_values(self) -> None:
        grid_size = self.num_columns * self.num_columns
        symbols_remaining = grid_size - len(self.grid_values)
        for i in range(symbols_remaining):
            symbol = roll(self.default_values)
            self.grid_values.append(symbol)

    def scratch_tiles(self, list_coordinates):
        super().scratch_tiles(list_coordinates)
        self._check_game_end()

    def _check_game_end(self) -> None:
        if self.attempts_remaining <= 0:
            self._check_results()
            self.payout = self.__calculate_payout()
            self.end_game()

    def _scratch(self, y, x):
        super()._scratch(y, x)
        chosen_symbol = self.grid_values[y][x]
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
            results = filter_value(results, results[0])

    def __calculate_payout(self) -> int:
        if self.winning_symbols:
            sum_payout = sum([self.get_value(symbol) for symbol in self.winning_symbols])
            num_winning_symbols = len(self.winning_symbols)
            total_payout = sum_payout * num_winning_symbols
            return int(math.floor(total_payout))
        return 0

    @staticmethod
    def get_value(symbol):
        return symbol['value']