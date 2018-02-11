from Core.constants import GAME_ID
from Core.helper_functions import *
from GridGames.grid import GridHandler, GridOptions
from GridGames.ScratchCard.Hammerpot.feedback import HammerpotFeedback
from GridGames.ScratchCard.Hammerpot.render_hammerpot import RenderHammerpot
from GridGames.ScratchCard.constants import *
from GridGames.ScratchCard.scratch_card import ScratchCard


class Hammerpot(ScratchCard):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.title = "HAMMERPOT"
        self.max_time_left = 180
        self.underlying_symbols = [ONE, TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE]
        self.attempts_remaining = 3
        self.possible_payouts = [1, 3, 5, 10, 15, 25, 50, 75, 100]
        self.winnable_payouts = {}
        self.winnable_sums = []
        self.chosen_sum = 0
        self.grid_handler = GridHandler(self.num_columns)
        self.card_renderer = None  # TBD
        self.id = GAME_ID["HAMMERPOT"]
        self.initialize_card()
        self.feedback = HammerpotFeedback(self)

    def initialize_card(self):
        super().initialize_card()
        self._initialize_sums()
        self._initialize_payouts()
        self._reveal_random_tile()
        self.card_renderer = RenderHammerpot(self)

    def pick_line(self, line: List[list]):
        fitted_line = line[:self.num_columns]
        tiles = self._get_tiles(fitted_line)
        self._reveal_line(fitted_line)
        self.chosen_sum = self._get_sum(tiles)
        self._end_game()

    def _end_game(self):
        self.payout = self._get_matching_payout()
        super().end_game()

    def _reveal_line(self, line):
        for coordinates in line:
            y = coordinates[0]
            x = coordinates[1]
            self._scratch(y, x)

    def _reveal_random_tile(self):
        y = self.get_random_coordinate()
        x = self.get_random_coordinate()
        self._reveal_tile(y, x)

    def get_random_coordinate(self):
            return random.randint(0, self.num_columns - 1)

    def _get_tiles(self, list_coordinates: List[list]):
        grid = self.underlying_symbols

        def get_tile(coordinates):
            y = coordinates[0]
            x = coordinates[1]
            return grid[y][x]
        return [get_tile(coordinates) for coordinates in list_coordinates]

    def _initialize_payouts(self):
        generated_payouts = self._generate_payouts()

        for i, sum_value in enumerate(self.winnable_sums):
            self.winnable_payouts[sum_value] = generated_payouts[i]

    def _generate_payouts(self):
        payouts = self._get_biased_payouts()
        num_payouts_needed = len(self.winnable_sums) - len(payouts)

        for i in range(num_payouts_needed):
            rolled_payout = roll(self.possible_payouts)
            self.possible_payouts.remove(rolled_payout)
            payouts.append(rolled_payout)

        random.shuffle(payouts)
        return payouts

    def _get_biased_payouts(self) -> List[int]:
        high_end = self._get_high_end_payout()
        low_end = self._get_low_end_payout()
        return [high_end, low_end]

    def _initialize_sums(self) -> None:
        # Records the unique sums of the numbers across each column, row and diagonal
        top_left_diagonal = self._get_top_left_diagonal_tiles()
        top_right_diagonal = self._get_top_right_diagonal_tiles()

        def _add_sum(tiles):
            value_sum = self._get_sum(tiles)
            if value_sum not in self.winnable_sums:
                self.winnable_sums.append(value_sum)

        [_add_sum(column) for column in self.underlying_symbols]
        [_add_sum(row) for row in self.underlying_symbols]
        _add_sum(top_left_diagonal)
        _add_sum(top_right_diagonal)

    def _get_top_left_diagonal_tiles(self) -> List[dict]:
        return self.grid_handler.get_top_left_diagonal(self.underlying_symbols)

    def _get_top_right_diagonal_tiles(self) -> List[dict]:
        return self.grid_handler.get_top_right_diagonal(self.underlying_symbols)

    def _get_sum(self, tiles) -> int:
        return sum([self.grid_handler.get_value(tile) for tile in tiles])

    def _get_low_end_payout(self) -> int:
        # Payout charts are guaranteed one low and one high payout
        low_end = roll(self.possible_payouts[:-3])
        self.possible_payouts.remove(low_end)
        return low_end

    def _get_high_end_payout(self) -> int:
        high_end = roll(self.possible_payouts[-3:])
        self.possible_payouts.remove(high_end)
        return high_end

    def _get_matching_payout(self) -> int:
        return self.winnable_payouts[self.chosen_sum]
