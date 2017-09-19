class SlotsFeedback:
    def __init__(self, slot_machine):
        self.slot_machine = slot_machine
        self.winning_symbols = slot_machine.winning_symbols

    def display_winning_symbols(self) -> str:
        return '\n'.join([self.get_stats(symbol) for symbol in self.winning_symbols])

    @staticmethod
    def get_stats(symbol: dict) -> str:
        return ': '.join([str(symbol[key]) for key in symbol])

    def get_win_report(self):
        winning_stats = self.display_winning_symbols()
        payout = self.get_payout()
        return self.slot_machine.get_win_message(winning_stats, payout)

    def get_payout(self) -> int:
        winning_symbols = self.winning_symbols
        sum_payout = sum([symbol['value'] for symbol in winning_symbols])
        num_winning_symbols = len(winning_symbols)
        return sum_payout * num_winning_symbols * self.slot_machine.payout_multiplier

    def get_outcome_report(self):
        if self.winning_symbols:
            return self.get_win_report()
        return self.slot_machine.get_lose_message()