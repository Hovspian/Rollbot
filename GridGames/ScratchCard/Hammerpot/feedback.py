class HammerpotFeedback:
    def __init__(self, hammerpot):
        self.hammerpot = hammerpot

    def get_card(self):
        host = self.hammerpot.host_name
        return '\n'.join([f":hammer: {host}'s Hammerpot :hammer:",
                          self.hammerpot.render_card()])

    def get_starting_message(self):
        return '\n'.join([f":hammer: Welcome to HAMMERPOT :hammer:",
                          self.hammerpot.render_card(),
                          "1. Reveal 3 tiles with `/scratch`",
                          "2. Then `/pick` a line (row, column, or diagonal)",
                          "The sum of the numbers on your selected line "
                          "corresponds to a payout in the chart!"])

    def get_report(self):
        if self.hammerpot.in_progress:
            return self._get_progress_report()
        return self._get_end_report()

    def _get_end_report(self) -> str:
        chosen_sum = self.hammerpot.chosen_sum
        payout = self.hammerpot.winnings
        return '\n'.join([f"Your sum is **{chosen_sum}**!",
                          f":hammer: Payout is {payout} gold. :hammer:"])

    def _get_progress_report(self):
        num = self.hammerpot.attempts_remaining
        if num > 0:
            return f'{num} remaining tiles to reveal.'
        else:
            return "\n".join(["Revealed all available tiles. Please `/pick` a line to get your sum. Examples:",
                              "Column: `/pick B`    Row: `/pick 2`",
                              "Diagonal from top-left: `/pick A0`    Diagonal from top-right: `/pick C0`"])
