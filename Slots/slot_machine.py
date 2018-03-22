import math

from Core.core_game_class import GameCore
from Core.helper_functions import *
from GridGames.grid import GridHandler
from Slots.bias_mechanic import SlotsBias
from Slots.feedback import SlotsFeedback
from Slots.result_checker import ResultChecker


class SlotMachine(GameCore):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.default_outcomes = []
        self.num_columns = self._init_num_columns()
        self.grid_handler = GridHandler(self.num_columns, self.num_columns)
        self.winning_combos = []
        self.winning_symbols = []
        self.payout = 0
        self.payout_multiplier = 1
        self.results = []  # Columns which are displayed to the user
        self.bias_mechanic = SlotsBias(self)

    def _init_num_columns(self) -> int:
        return 3

    def run(self) -> None:
        self._generate_columns()
        self._check_results()
        self._resolve_payout()

    def _generate_columns(self):
        first_column = self._get_initial_column()
        self.results.append(first_column)
        for i in range(self.num_columns - 1):
            reel = self._reconstruct_reel()
            column = self._generate_column(reel)
            self.results.append(column)

    def render_slots(self) -> str:
        rows = self.grid_handler.get_rows(self.results)
        symbols = [self.grid_handler.get_emotes(row) for row in rows]
        return '\n'.join(symbols)

    def get_outcome_report(self) -> str:
        return SlotsFeedback(self).get_outcome_report()

    def get_payout(self) -> int:
        return self.payout

    def _check_results(self) -> None:
        result_checker = ResultChecker(self)
        result_checker.analyze_results()

    def _resolve_payout(self):
        self.payout += self._calculate_payout()

    def _calculate_payout(self) -> int:
        winning_symbols = self.winning_symbols
        if winning_symbols:
            sum_payout = sum([self.grid_handler.get_value(symbol) for symbol in winning_symbols])
            total_payout = sum_payout * len(winning_symbols) * self.payout_multiplier
            return int(math.floor(total_payout))
        return 0

    def _reconstruct_reel(self) -> List[dict]:
        new_reel = list(self.results[0])
        symbols_left = self.num_columns + 1
        for i in range(symbols_left):
            symbol = self._get_symbol(new_reel)
            new_reel.append(symbol)
        return new_reel

    def _get_initial_column(self) -> List[dict]:
        column = []
        for i in range(self.num_columns):
            symbol = self.get_initial_reel_symbol(column)
            column.append(symbol)
        return column

    def get_initial_reel_symbol(self, reel: List[dict]) -> dict:
        if len(reel) > 0:
            previous_symbol = reel[len(reel) - 1]
            filtered_container = filter_value(container=self.default_outcomes, value_to_filter=previous_symbol)
            return roll(filtered_container)
        else:
            return roll(self.default_outcomes)

    def _get_symbol(self, reel: List[dict]) -> dict:
        biased_symbol = self.bias_mechanic.get_symbol_to_match()
        previous_symbol = reel[len(reel) - 1]
        rolled_num = roll([0, 1, 1, 1, 1, 1])
        if biased_symbol is previous_symbol or rolled_num == 1:
            return self._get_random_symbol(reel)
        return biased_symbol

    def _get_random_symbol(self, reel: List[dict]) -> dict:
        """
        Returns a symbol that is either biased or random from the default symbol pool.
        """
        first_column = self.results[0]
        previous_symbol = reel[len(reel) - 1]
        containers = [first_column, first_column, first_column, self.default_outcomes]
        # Pick a random container and filter the previous symbol from it:
        symbols = filter_value(roll(containers), previous_symbol)
        return roll(symbols)

    def _generate_column(self, reel: List[dict]) -> List[dict]:
        # A column, the tiles visible to the player, is a subsection of a reel
        column = []
        index = self.bias_mechanic.get_index(reel)
        for i in range(self.num_columns):
            column.append(reel[index])
            index += 1
            index = loop_list_value(index, container=reel)
        return column
