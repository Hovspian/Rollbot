class ScratchCardFeedback:
    # String builders
    def __init__(self, scratch_card):
        self.scratch_card = scratch_card

    def get_card(self):
        host = self.scratch_card.host_name
        return '\n'.join([f"{host}'s scratch card",
                          self.scratch_card.render_card()])

    def get_starting_message(self) -> str:
        host = self.scratch_card.host_name
        num_symbols = self.scratch_card.matches_to_win
        num_attempts = self.scratch_card.attempts_remaining
        return '\n'.join([f'New scratch card for {host}.',
                          self.scratch_card.render_card(),
                          f'Match {num_symbols} symbols to win!',
                          f'You have {num_attempts} attempts remaining.'])

    def get_report(self):
        if self.scratch_card.in_progress:
            return self._get_progress_report()
        return self._get_end_report()

    def _get_end_report(self) -> str:
        if self.scratch_card.winning_symbols:
            return self._get_winning_report()
        return 'Sorry, not a winning game.'

    def _get_winning_report(self) -> str:
        winning_symbols = self.scratch_card.winning_symbols
        payout_stats = '\n'.join([self._symbol_stats(match) for match in winning_symbols])
        payout = self.scratch_card.calculate_payout()
        payout_message = f':dollar: Payout is {payout} gold. :dollar:'
        return '\n'.join(["Winning match!", payout_stats, payout_message])

    @staticmethod
    def _symbol_stats(symbol) -> str:
        return ': '.join([str(symbol[key]) for key in symbol])

    def _get_progress_report(self):
        num = self.scratch_card.attempts_remaining
        if num > 1:
            return f'{num} attempts remaining.'
        return '1 attempt remaining.'
