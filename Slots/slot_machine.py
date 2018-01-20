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
        self.num_columns = 3
        self.results_grid = GridHandler(self.num_columns)
        self.first_reel_size = int(math.ceil(self.num_columns * 1.5))
        self.reels = []
        self.winning_combos = []
        self.winning_symbols = []
        self.payout_amount = 0
        self.payout_multiplier = 1
        self.results = []
        self.bias_mechanic = SlotsBias(self)

    def run(self) -> None:

        def _roll_columns() -> None:
            reel = self._get_reel()
            column = self._generate_column(reel)
            self.results_grid.add_column(column)

        [_roll_columns() for i in range(self.num_columns)]
        self.results = self.results_grid.get_grid()
        self._check_results()
        self._resolve_payout()

    def render_slots(self) -> str:
        rows = self.results_grid.get_rows()
        symbols = [self.results_grid.get_emotes(row) for row in rows]
        return '\n'.join(symbols)

    def get_outcome_report(self) -> str:
        return SlotsFeedback(self).get_outcome_report()

    def get_payout_amount(self) -> int:
        return self.payout_amount

    def _check_results(self) -> None:
        result_checker = ResultChecker(self)
        result_checker.analyze_results()

    def _resolve_payout(self):
        self.payout_amount += self._calculate_payout()

    def _calculate_payout(self) -> int:
        winning_symbols = self.winning_symbols
        if winning_symbols:
            sum_payout = sum([self.results_grid.get_value(symbol) for symbol in winning_symbols])
            num_winning_symbols = len(winning_symbols)
            total_payout = sum_payout * num_winning_symbols * self.payout_multiplier
            return int(math.floor(total_payout))
        return 0

    def _get_reel(self) -> List[dict]:
        # If no reel, create one from default values. Otherwise, reconstruct the first reel.
        if not self.reels:
            reel = self._roll_initial_reel()
        else:
            reel = self._rebuild_reel()
        self.reels.append(reel)
        return reel

    def _roll_initial_reel(self) -> List[dict]:
        return self._generate_reel(self.default_outcomes, self.first_reel_size)

    def _rebuild_reel(self) -> List[dict]:
        first_column = self.results_grid.columns[0]
        first_reel = self.reels[0]
        include_symbols = self._roll_num_included_symbols()
        rerolled_reel = self._generate_reel(first_reel, include_symbols)
        return rerolled_reel + first_column

    @staticmethod
    def _generate_reel(symbols, reel_size) -> List[dict]:
        reel = []

        def roll_add_to_reel(i) -> dict:
            symbol = get_symbol(i)
            return symbol

        def get_symbol(i) -> dict:
            previous_symbol = get_previous_symbol(i)
            if previous_symbol:
                filtered_container = filter_value(container=symbols, value_to_filter=previous_symbol)
                symbol = roll(filtered_container)
            else:
                symbol = roll(symbols)
            return symbol

        def get_previous_symbol(i) -> dict:
            if reel:
                previous_symbol = reel[i - 1]
                return previous_symbol

        return [roll_add_to_reel(i) for i in range(reel_size)]

    def _roll_num_included_symbols(self) -> int:
        return random.randint(1, self.num_columns + 1)

    def _generate_column(self, reel) -> List[dict]:
        # A column, the tiles visible to the player, is a subsection of a reel
        column = []
        index = self.bias_mechanic.get_index(reel)

        for i in range(self.num_columns):
            column.append(reel[index])
            index += 1
            index = loop_list_value(index, container=reel)
        return column
