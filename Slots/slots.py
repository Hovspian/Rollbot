import random
from typing import List


class SlotMachine:
    def __init__(self, author):
        self.player = author
        self.num_rows = 3
        self.winning_symbols = []
        self.results = []
        self.cherry = {'emote': ':cherries:', 'value': 1}
        self.angel = {'emote': ':angel:', 'value': 3}
        self.pear = {'emote': ':pear:', 'value': 5}
        self.pineapple = {'emote': ':pineapple:', 'value': 7}
        self.butt = {'emote': ':peach:', 'value': 10}
        self.meat = {'emote': ':meat_on_bone:', 'value': 15}
        self.hammer = {'emote': ':hammer:', 'value': 25}
        self.seven = {'emote': ':seven:', 'value': 100}

    def get_outcomes(self):
        return [self.cherry, self.cherry,
                self.angel, self.angel,
                self.pear, self.pear,
                self.pineapple,
                self.butt,
                self.meat,
                self.hammer,
                self.seven]

    def play_slot(self) -> None:
        self.results = [self.roll_row() for i in range(self.num_rows)]
        self.analyze_results()

    def compile_report(self) -> str:
        linebreak = '\n'
        label = "| {}'s slot results |".format(self.player)
        slot_machine = self.draw_slot_interface(self.results)
        outcome = self.get_outcome_report()
        return linebreak.join([label, slot_machine, outcome])

    def roll_row(self) -> List[dict]:
        return [self.roll() for i in range(self.num_rows)]

    def roll(self) -> dict:
        symbols = self.get_outcomes()
        pick = random.randint(0, len(symbols) - 1)
        return symbols[pick]

    def analyze_results(self) -> None:
        [self.check_winning_match(row) for row in self.results]
        self.check_top_left_diagonal(self.results)
        self.check_top_right_diagonal(self.results)

    def check_top_left_diagonal(self, results) -> None:
        top_left_diagonal = self.get_diagonal(results)
        self.check_winning_match(top_left_diagonal)

    def check_top_right_diagonal(self, results) -> None:
        reversed_rows = reversed(results)
        top_right_diagonal = self.get_diagonal(reversed_rows)
        self.check_winning_match(top_right_diagonal)

    @staticmethod
    def get_diagonal(rows) -> List[dict]:
        return [row[i] for i, row in enumerate(rows)]

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

    def draw_slot_interface(self, results) -> str:
        return '\n'.join([self.get_emotes(row) for row in results])

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
