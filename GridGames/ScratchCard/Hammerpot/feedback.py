from GridGames.ScratchCard.Hammerpot.render_hammerpot import RenderHammerpot


class HammerpotFeedback:
    def __init__(self, hammerpot):
        self.hammerpot = hammerpot
        self.renderer = RenderHammerpot(self)

    def get_card(self):
        host = self.hammerpot.host_name
        return '\n'.join([f":hammer: {host}'s Hammerpot :hammer:",
                          self.renderer.render_card()])

    def get_starting_message(self):
        title = self.hammerpot.title
        num_attempts = self.hammerpot.attempts_remaining
        numbers = self.hammerpot.num_columns * self.hammerpot.num_columns
        return '\n'.join([f":hammer: Welcome to {title} :hammer:",
                          self.renderer.render_card(),
                          f"This card contains unique numbers from 1 to {numbers}.",
                          f"1. Reveal {num_attempts} tiles with `/scratch`",
                          "2. Then `/pick` a line (row, column, or diagonal)",
                          "The sum of the numbers across your selected line "
                          "matches a payout in the chart!"])

    def get_report(self):
        if self.hammerpot.in_progress:
            return self._get_progress_report()
        return self._get_end_report()

    def _get_end_report(self) -> str:
        chosen_sum = self.hammerpot.chosen_sum
        payout = self.hammerpot.payout
        return '\n'.join([f"Your sum is {chosen_sum}!",
                          f":hammer: Payout is {payout} gold. :hammer:"])

    def _get_progress_report(self):
        num_attempts = self.hammerpot.attempts_remaining
        if num_attempts == 1:
            return 'One tile left!'
        elif num_attempts > 1:
            return f'{num_attempts} remaining tiles to reveal.'
        else:
            return "\n".join(["Revealed all available tiles. Please `/pick` a line to get your sum. Examples:",
                              "Column: `/pick B`    Row: `/pick 2`",
                              "Diagonal from top-left: `/pick A0`    Diagonal from top-right: `/pick C0`"])
