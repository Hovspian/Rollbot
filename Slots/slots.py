import random
from typing import List

cherry = {'emote': ':cherries:', 'value': 1}
angel = {'emote': ':angel:', 'value': 3}
pear = {'emote': ':pear:', 'value': 5}
pineapple = {'emote': ':pineapple:', 'value': 7}
butt = {'emote': ':peach:', 'value': 10}
meat = {'emote': ':meat_on_bone:', 'value': 15}
hammer = {'emote': ':hammer:', 'value': 25}
seven = {'emote': ':seven:', 'value': 100}


class SlotMachine:
    def __init__(self, author):
        self.player = author
        self.num_columns = 3
        self.winning_symbols = []
        self.results = []

    @staticmethod
    def get_outcomes():
        return [cherry, cherry,
                angel, angel,
                pear, pear,
                pineapple,
                butt,
                meat,
                bar, bar,
                hammer,
                cake,
                seven]

    def play_slot(self) -> None:
        first_column = self.roll_column()
        self.add_result(first_column)

        def perform_rolls(previous_column):
            next_column = self.roll_column(previous_column)
            self.add_result(next_column)

        [perform_rolls(self.results[previous]) for previous in range(self.num_columns - 1)]
        self.analyze_results()

    def add_result(self, column):
        self.results.append(column)

    def compile_report(self) -> str:
        linebreak = '\n'
        label = "| {}'s slot results |".format(self.player)
        slot_machine = self.draw_slot_interface()
        outcome = self.get_outcome_report()
        return linebreak.join([label, slot_machine, outcome])

    def roll_column(self, previous_column=None) -> List[dict]:

        def roll_symbols(i):
            symbol_lists = self.get_symbol_lists(i, previous_column)
            return self.roll(symbol_lists)
        return [self.roll(roll_symbols(i)) for i in range(self.num_columns)]

    def get_symbol_lists(self, i, previous_column=None):
        normal_outcomes = self.get_outcomes()
        roll_types = [normal_outcomes, normal_outcomes, normal_outcomes]
        if previous_column:
            roll_types.append(previous_column)
            roll_types.append([previous_column[i]])
        return roll_types

    @staticmethod
    def roll(input_list: List) -> any:
        pick = random.randint(0, len(input_list) - 1)
        return input_list[pick]

    def analyze_results(self) -> None:
        self.check_rows()
        self.check_top_left_diagonal()
        self.check_top_right_diagonal()

    def check_columns(self):
        [self.check_winning_match(column) for column in self.results]

    def check_rows(self):
        [self.check_winning_match(row) for row in self.get_rows()]

    def get_rows(self):
        def get_row(column):
            row = [self.results[i][column] for i in range(self.num_columns)]
            return row
        return [get_row(column) for column in range(self.num_columns)]

    def check_top_left_diagonal(self) -> None:
        top_left_diagonal = self.get_diagonal(self.results)
        self.check_winning_match(top_left_diagonal)

    def check_top_right_diagonal(self) -> None:
        reversed_columns = reversed(self.results)
        top_right_diagonal = self.get_diagonal(reversed_columns)
        self.check_winning_match(top_right_diagonal)

    @staticmethod
    def get_diagonal(columns) -> List[dict]:
        return [column[i] for i, column in enumerate(columns)]

    def check_winning_match(self, symbols: List[dict]) -> None:
        if self.is_winning_match(symbols):
            self.add_winning_match(symbols[0])

    @staticmethod
    def is_winning_match(symbols) -> bool:
        for symbol in symbols:
            if symbol != symbols[0]:
                return False
        return True

    def add_winning_match(self, symbol: dict) -> None:
        self.winning_symbols.append(symbol)

    def has_winnings(self) -> bool:
        return len(self.winning_symbols) > 0

    def get_payout(self) -> int:
        sum_payout = sum([symbol['value'] for symbol in self.winning_symbols])
        num_winning_symbols = len(self.winning_symbols)
        return sum_payout * num_winning_symbols

    def get_winning_symbols(self) -> List[str]:
        return [self.get_stats(symbol) for symbol in self.winning_symbols]

    @staticmethod
    def get_stats(symbol: dict) -> str:
        return ': '.join([str(symbol[key]) for key in symbol])

    def draw_slot_interface(self) -> str:
        rows = self.get_rows()
        return '\n'.join([self.get_emotes(row) for row in rows])

    @staticmethod
    def get_emotes(symbols) -> str:
        return ''.join([symbol['emote'] for symbol in symbols])

    def get_outcome_report(self) -> str:
        if self.has_winnings():
            return self.get_win_report()
        return 'Sorry, not a winning game.'

    def get_win_report(self) -> str:
        linebreak = '\n'
        winning_stats = linebreak.join(self.get_winning_symbols())
        payout = self.get_payout()
        return linebreak.join(['Rolled a match!', f'{winning_stats}', f':dollar: Payout is {payout} gold. :dollar:'])
