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
        self.grid_handler = GridHandler(self.num_columns)
        self.first_reel_size = int(math.ceil(self.num_columns * 1.5))
        self.reels = []
        self.winning_combos = []
        self.winning_symbols = []
        self.payout = 0
        self.payout_multiplier = 1
        self.results = self.grid_handler.get_grid()
        self.bias_mechanic = SlotsBias(self)

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
        first_column = self.grid_handler.columns[0]
        first_reel = self.reels[0]
        reel_size = self._roll_num_included_symbols()
        rerolled_reel = self._generate_reel(first_reel, reel_size)
        return rerolled_reel + first_column

    @staticmethod
    def _generate_reel(from_reel, reel_size) -> List[dict]:
        new_reel = []

        def get_symbol(i) -> dict:
            if len(new_reel) > 1:
                previous_symbol = new_reel[i - 1]
                filtered_container = filter_value(container=from_reel, value_to_filter=previous_symbol)
                result = roll(filtered_container)
                return result
            else:
                return roll(from_reel)

        for i in range(reel_size):
            symbol = get_symbol(i)
            new_reel.append(symbol)
        return new_reel

    def _roll_num_included_symbols(self) -> int:
        return random.randint(1, self.num_columns + 1)

    def _generate_column(self, reel) -> List[dict]:
        # A column, the tiles visible to the player, is a subsection of a reel
        column = []
        index = self.bias_mechanic.get_index(reel)
        # print(index)

        for i in range(self.num_columns):
            column.append(reel[index])
            index += 1
            index = loop_list_value(index, container=reel)
        return column
