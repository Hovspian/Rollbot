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
        self.num_columns = self.init_num_columns()
        self.grid_handler = GridHandler(self.num_columns, self.num_columns)
        self.first_reel_size = self.num_columns
        self.reels = []
        self.winning_combos = []
        self.winning_symbols = []
        self.payout = 0
        self.results = self.grid_handler.get_grid()
        self.bias_mechanic = SlotsBias(self)

    def init_num_columns(self) -> int:
        return 3

    def run(self) -> None:

        def _roll_columns() -> None:
            reel = self._get_reel()
            column = self._generate_column(reel)
            self.grid_handler.add_column(column)

        [_roll_columns() for i in range(self.num_columns)]
        self._check_results()
        self._resolve_payout()

    def render_slots(self) -> str:
        rows = self.grid_handler.get_rows()
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
            total_payout = sum_payout
            return int(math.floor(total_payout))
        return 0

    def _get_reel(self) -> List[dict]:
        # If no reel, create one from default values. Otherwise, reconstruct the first reel.
        if len(self.reels) == 0:
            reel = self._roll_initial_reel()
        else:
            reel = self._rebuild_reel()
        self.reels.append(reel)
        return reel

    def _roll_initial_reel(self) -> List[dict]:
        reel = []
        for i in range(self.first_reel_size):
            symbol = self.get_initial_reel_symbol(reel)
            reel.append(symbol)
        return reel

    def get_initial_reel_symbol(self, reel: List[dict]) -> dict:
        if len(reel) > 0:
            previous_symbol = reel[len(reel) - 1]
            filtered_container = filter_value(container=self.default_outcomes, value_to_filter=previous_symbol)
            return roll(filtered_container)
        else:
            return roll(self.default_outcomes)

    def _rebuild_reel(self) -> List[dict]:
        new_reel = list(self.grid_handler.columns[0])
        first_reel = self.reels[0]
        symbols_left = self._roll_num_included_symbols()
        for i in range(symbols_left):
            previous_symbol = new_reel[len(new_reel) - 1]
            filtered_container = filter_value(container=first_reel, value_to_filter=previous_symbol)
            symbol = roll(filtered_container)
            new_reel.append(symbol)
        return new_reel

    def _roll_num_included_symbols(self) -> int:
        return random.randint(2, self.num_columns)

    def _generate_column(self, reel) -> List[dict]:
        # A column, the tiles visible to the player, is a subsection of a reel
        column = []
        index = self.bias_mechanic.get_index(reel)

        for i in range(self.num_columns):
            column.append(reel[index])
            index += 1
            index = loop_list_value(index, container=reel)
        return column
