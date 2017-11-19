import math
from typing import List

from Core.joinable_game_class import JoinableGame


class GridGame(JoinableGame):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.num_columns = 3
        self.payout_multiplier = 1
        self.results = []
        self.winning_symbols = []
        self.host = ctx.message.author

    def get_rows(self, columns) -> List[list]:
        def _get_row(i):
            return [columns[column][i] for column in range(self.num_columns)]
        return [_get_row(i) for i in range(self.num_columns)]

    def get_emotes(self, symbols) -> str:
        return ''.join(self.get_emote_list(symbols))

    def get_emote_list(self, symbols):
        return [self.get_emote(symbol) for symbol in symbols]

    @staticmethod
    def get_emote(symbol):
        return symbol['emote']

    @staticmethod
    def get_value(symbol):
        return symbol['value']

    def calculate_payout(self) -> int:
        if self.winning_symbols:
            sum_payout = sum([self.get_value(symbol) for symbol in self.winning_symbols])
            num_winning_symbols = len(self.winning_symbols)
            total_payout = sum_payout * num_winning_symbols * self.payout_multiplier
            return int(math.floor(total_payout))
        return 0

