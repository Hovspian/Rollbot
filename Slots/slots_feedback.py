class SlotsFeedback:
    def __init__(self, slot_machine):
        self.winning_symbols = slot_machine.winning_symbols
        self.winning_combos = slot_machine.winning_combos
        self.win_message = slot_machine.get_win_message
        self.lose_message = slot_machine.get_lose_message
        self.payout_multiplier = slot_machine.payout_multiplier

    def display_winning_symbols(self) -> str:
        return '\n'.join([self.get_stats(symbol, i) for i, symbol in enumerate(self.winning_symbols)])

    def get_stats(self, symbol: dict, i: int) -> str:
        combo_name = self.winning_combos[i]

        def symbol_stats():
            return ': '.join([str(symbol[key]) for key in symbol])
        return ' - '.join([symbol_stats(), combo_name])

    def get_win_report(self):
        matches = self.winning_combos_message()
        winning_stats = self.display_winning_symbols()
        payout = self.get_payout()
        return self.win_message(matches, winning_stats, payout)

    def winning_combos_message(self):
        num_combos = len(self.winning_combos)
        if num_combos > 1:
            return ' '.join([str(num_combos), 'matches'])
        return 'a match'

    def get_payout(self) -> int:
        sum_payout = sum([symbol['value'] for symbol in self.winning_symbols])
        num_winning_symbols = len(self.winning_symbols)
        return sum_payout * num_winning_symbols * self.payout_multiplier

    def get_outcome_report(self):
        if self.winning_symbols:
            return self.get_win_report()
        return self.lose_message()