class SlotsFeedback:
    def __init__(self, slot_machine):
        self.winning_symbols = slot_machine.winning_symbols
        self.winning_combos = slot_machine.winning_combos
        self.win_message = slot_machine.get_win_message
        self.payout = slot_machine.payout

    def get_outcome_report(self):
        if self.winning_symbols:
            return self._get_win_report()
        return 'Sorry, not a winning game.'

    def _display_winning_symbols(self) -> str:
        return '\n'.join([self._get_stats(symbol, i) for i, symbol in enumerate(self.winning_symbols)])

    def _get_stats(self, symbol: dict, i: int) -> str:
        combo_name = self.winning_combos[i]

        def _symbol_stats():
            return ': '.join([str(symbol[key]) for key in symbol])
        return ' - '.join([_symbol_stats(), combo_name])

    def _get_win_report(self):
        matches = self._winning_combos_message()
        winning_stats = self._display_winning_symbols()
        return self.win_message(matches, winning_stats, self.payout)

    def _winning_combos_message(self):
        num_combos = len(self.winning_combos)
        if num_combos > 1:
            return ' '.join([str(num_combos), 'matches'])
        return 'a match'
