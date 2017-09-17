import random
from typing import List


class SlotMachine:
    def __init__(self, author):
        self.player = author
        self.num_rows = 3
        self.winning_symbols = []
        self.cherry = {'emote': ':cherries:', 'value': 1}
        self.angel = {'emote': ':angel:', 'value': 3}
        self.pear = {'emote': ':pear:', 'value': 5}
        self.pineapple = {'emote': ':pineapple:', 'value': 7}
        self.butt = {'emote': ':peach:', 'value': 10}
        self.meat = {'emote': ':meat_on_bone:', 'value': 15}
        self.hammer = {'emote': ':hammer:', 'value': 25}
        self.seven = {'emote': ':seven:', 'value': 100}

    def get_outcomes(self):
        return [self.cherry, self.cherry, self.cherry,
                self.angel, self.angel, self.angel,
                self.pear, self.pear,
                self.pineapple, self.pineapple,
                self.butt, self.butt,
                self.meat, self.meat,
                self.hammer, self.hammer,
                self.seven]

    def play_slot(self):
        linebreak = '\n'
        results = [self.roll_row() for i in range(self.num_rows)]
        self.analyze_results(results)
        label = "| {}'s slot results |".format(self.player)
        return linebreak.join([label, self.draw_slot_interface(results), self.get_outcome_report()])

    def roll_row(self):
        return [self.roll() for i in range(self.num_rows)]

    def roll(self):
        outcomes = self.get_outcomes()
        pick = random.randint(0, len(outcomes) - 1)
        return outcomes[pick]

    def analyze_results(self, results):
        for result in results:
            self.is_winning_match(result)
        self.check_diagonals(results)

    def check_diagonals(self, results):
        middle_result = self.get_middle_result(results)
        first_row = self.get_first_of(results)
        last_row = self.get_last_of(results)
        top_left = self.top_left_diagonal(first_row, middle_result, last_row)
        top_right = self.top_right_diagonal(first_row, middle_result, last_row)
        self.is_winning_match(top_left)
        self.is_winning_match(top_right)

    def top_left_diagonal(self, first_row, middle_result, last_row):
        top_left = self.get_first_of(first_row)
        bottom_right = self.get_last_of(last_row)
        return [top_left, middle_result, bottom_right]

    def top_right_diagonal(self, first_row, middle_result, last_row):
        top_right = self.get_last_of(first_row)
        bottom_left = self.get_first_of(last_row)
        return [top_right, middle_result, bottom_left]

    @staticmethod
    def get_last_of(items):
        last = len(items) - 1
        return items[last]

    @staticmethod
    def get_first_of(items):
        return items[0]

    @staticmethod
    def get_middle_of(items):
        num_items = len(items) - 1
        pick_middle = num_items - int(num_items / 2)
        return items[pick_middle]

    def get_middle_result(self, results):
        middle_row = self.get_middle_of(results)
        return self.get_middle_of(middle_row)

    def is_winning_match(self, symbols: List[dict]):
        first_item = symbols[0]
        for item in symbols:
            if item != first_item:
                return
        self.add_winning_match(first_item)

    def add_winning_match(self, symbol: dict):
        self.winning_symbols.append(symbol)

    def has_winnings(self):
        if len(self.winning_symbols) > 0:
            return True

    def get_payout(self):
        payout = 0
        for symbol in self.winning_symbols:
            payout += symbol['value']
        return payout

    def get_winning_symbols(self):

        def get_stats(symbol):
            emote = symbol['emote']
            value = str(symbol['value'])
            return ': '.join([emote, value])
        return [get_stats(symbol) for symbol in self.winning_symbols]

    def draw_slot_interface(self, results):
        linebreak = '\n'
        first_row = self.get_first_of(results)
        middle_row = self.get_middle_of(results)
        last_row = self.get_last_of(results)

        def get_emotes(symbol_list):
            return ''.join([symbol['emote'] for symbol in symbol_list])

        return linebreak.join([get_emotes(first_row), get_emotes(middle_row), get_emotes(last_row)])

    def get_outcome_report(self):
        if self.has_winnings():
            linebreak = '\n'
            winning_stats = linebreak.join(self.get_winning_symbols())
            payout = self.get_payout()
            return f":dollar: Rolled a match! \n{winning_stats} \n Payout is {payout} gold. :dollar:"
        else:
            return "Sorry, not a winning game."