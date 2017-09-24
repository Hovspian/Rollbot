import random
import math
from typing import List


class GridGame:
    def __init__(self):
        self.num_columns = 3
        self.payout_multiplier = 1
        self.results = []
        self.winning_symbols = []

    def get_rows(self, columns) -> List[list]:
        def _get_row(i):
            return [columns[column][i] for column in range(self.num_columns)]
        return [_get_row(i) for i in range(self.num_columns)]

    @staticmethod
    def remove_symbol(container, filter_symbol):
        return [symbol for symbol in container if symbol != filter_symbol]

    @staticmethod
    def _roll(input_list: List) -> any:
        pick = random.randint(0, len(input_list) - 1)
        return input_list[pick]

    def get_emotes(self, symbols) -> str:
        return ''.join([self.get_emote(symbol) for symbol in symbols])

    @staticmethod
    def get_emote(symbol):
        return symbol['emote']

    @staticmethod
    def split_input(message):
        return message.split(',')

    @staticmethod
    def remove_symbol(container, filter_symbol):
        return [symbol for symbol in container if symbol != filter_symbol]

    def calculate_payout(self) -> int:
        if self.winning_symbols:
            sum_payout = sum([symbol['value'] for symbol in self.winning_symbols])
            num_winning_symbols = len(self.winning_symbols)
            return sum_payout * num_winning_symbols * self.payout_multiplier
        return 0