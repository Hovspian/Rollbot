import math

from GridGames.Slots.bias_mechanic import SlotsBias
from GridGames.Slots.feedback import SlotsFeedback
from GridGames.Slots.result_checker import ResultChecker
from GridGames.grid_game_class import GridGame
from helper_functions import *


class SlotMachine(GridGame):

    def __init__(self, ctx):
        super().__init__(ctx)
        self.default_outcomes = []
        self.first_reel_size = int(math.ceil(self.num_columns * 1.5))
        self.reels = []
        self.winning_combos = []
        self.payout_amount = 0
        self.bias_mechanic = SlotsBias(self)

    def play_slot(self) -> None:

        def _roll_columns() -> None:
            reel = self._get_reel()
            column = self._generate_column(reel)
            self._add_result(column)

        [_roll_columns() for i in range(self.num_columns)]
        self._check_results()
        self._resolve_payout()

    def draw_slot_interface(self) -> str:
        rows = super().get_rows(self.results)
        symbols = [self.get_emotes(row) for row in rows]
        return '\n'.join(symbols)

    def get_outcome_report(self) -> str:
        return SlotsFeedback(self).get_outcome_report()

    def get_payout_amount(self) -> int:
        return self.payout_amount

    def _check_results(self) -> None:
        result_checker = ResultChecker(self)
        result_checker.analyze_results()

    def _resolve_payout(self):
        self.payout_amount += self.calculate_payout()

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
        first_column = self.results[0]
        first_reel = self.reels[0]
        include_symbols = self._roll_num_included_symbols()
        rerolled_reel = self._generate_reel(first_reel, include_symbols)
        return rerolled_reel + first_column

    @staticmethod
    def _generate_reel(symbols, reel_size) -> List[dict]:
        reel = []

        def roll_add_to_reel(i) -> None:
            symbol = get_symbol(i)
            reel.append(symbol)

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

        [roll_add_to_reel(i) for i in range(reel_size)]
        return reel

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

    def _add_result(self, column) -> None:
        self.results.append(column)
