import math
import random
from typing import List
from GridGames.Slots.slot_feedback import SlotsFeedback
from GridGames.Slots.result_checker import ResultChecker
from GridGames.grid_game_class import GridGame
from GridGames.Slots.bias_mechanic import SlotsBias


class SlotMachine(GridGame):
    def __init__(self):
        super().__init__()
        self.default_outcomes = []
        self.first_reel_size = int(math.ceil(self.num_columns * 1.5))
        self.reels = []
        self.winning_combos = []
        self.payout_amount = 0
        self.bias_mechanic = SlotsBias(self)

    def play_slot(self) -> None:
        self.bias_mechanic.initialize()

        def _roll_columns() -> None:
            reel = self.generate_reel()
            column = self._generate_column(reel)
            self._add_result(column)

        [_roll_columns() for i in range(self.num_columns)]
        self._check_results()

    def draw_slot_interface(self) -> str:
        rows = super().get_rows(self.results)

        return '\n'.join([self.get_emotes(row) for row in rows])

    def get_outcome_report(self) -> str:
        return SlotsFeedback(self).get_outcome_report()

    def _check_results(self) -> None:
        result_checker = ResultChecker(self)
        result_checker.analyze_results()
        self.payout_amount += self.calculate_payout()

    def _roll_reel(self, symbols) -> List[dict]:
        reel = []

        def roll_add_to_reel(i):
            previous_symbol = get_previous_symbol(i)
            if previous_symbol:
                filtered_container = self.remove_value_from(symbols, previous_symbol)
                symbol = self._roll(filtered_container)
            else:
                symbol = self._roll(symbols)
            reel.append(symbol)

        def get_previous_symbol(i):
            if len(reel) > 0:
                previous_symbol = reel[i - 1]
                return previous_symbol

        [roll_add_to_reel(i) for i in range(self.first_reel_size)]
        return reel

    def generate_reel(self):
        # If no reel, create one from default values. Otherwise, reconstruct the first reel.
        if not self.reels:
            reel = self._roll_initial_reel()
        else:
            reel = self._rebuild_reel()
        self.reels.append(reel)
        return reel

    def _roll_initial_reel(self):
        initial_reel = self._roll_reel(self.default_outcomes)
        self.reels.append(initial_reel)
        return initial_reel

    def _rebuild_reel(self) -> List[dict]:
        first_column = self.results[0]
        first_reel = self.reels[0]
        rerolled_reel = self._roll_reel(first_reel)
        exclude_symbols = self._get_exclude_symbols()
        return rerolled_reel[:exclude_symbols] + first_column

    def _get_exclude_symbols(self):
        return random.randint(1, self.num_columns + 1)

    def _generate_column(self, reel) -> List[dict]:
        column = []
        index = self.get_starting_index(reel)

        for i in range(self.num_columns):
            column.append(reel[index])
            index = self._loop_reel_value(index + 1)
        return column

    def get_starting_index(self, reel):
        return self.bias_mechanic.get_index(reel)

    def _loop_reel_value(self, index) -> int:
        previous_reel_index = len(self.reels) - 1
        previous_reel_size = len(self.reels[previous_reel_index])
        return index % previous_reel_size

    def _add_result(self, column) -> None:
        self.results.append(column)
