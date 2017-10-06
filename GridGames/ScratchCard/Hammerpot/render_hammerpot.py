from GridGames.render_card import RenderCard
from GridGames.ScratchCard.Hammerpot.constants import *
from typing import List


class RenderHammerpot(RenderCard):
    # Renders the payout table next to the card

    def __init__(self, card):
        super().__init__(card)
        self.payout_table = self.get_payout_table()

    def render_card(self):
        card = self.get_card_rows()
        combined_rows = []
        for i in range(len(card)):
            row = SPACER.join([card[i], self.payout_table[i]])
            combined_rows.append(row)
        combined_rows = LINEBREAK.join(combined_rows)
        return combined_rows

    def get_payout_table(self):
        # Number of rows should be equal to the scratch card
        rows = self.get_payout_rows()
        table_bottom = self.get_table_bottom(rows)
        table = [TABLE_HEADER, TABLE_WHITESPACE] + rows + table_bottom
        return table

    def get_table_bottom(self, rows):
        # Depending on the number of rows for sum : payout entries, the bottom of the table needs to be taller
        rows_needed = 6 - len(rows)
        table_bottom = []
        for i in range(rows_needed):
            if i == rows_needed - 1:
                table_bottom.append(TABLE_BOTTOM)
            else:
                table_bottom.append(TABLE_WHITESPACE)
        return table_bottom

    def get_payout_rows(self):
        entries = self.get_payout_pairs()
        rows = []
        for entry in entries:
            payout_row = TABLE_PLACEHOLDER.format(*entry)
            rows.append(payout_row)
        return rows

    def get_payout_pairs(self):
        # A sum-payout entry has 8 characters, eg. 21 : 500
        formatted_payouts = self.get_formatted_payouts()
        entries = self.check_odd_num_entries(formatted_payouts)
        num_rows = len(formatted_payouts) // 2
        pairs = []

        for i in range(num_rows):
            slice_start = 0 + i * 2
            slice_end = 2 + i * 2
            pairs.append(entries[slice_start:slice_end])

        return pairs

    @staticmethod
    def check_odd_num_entries(formatted_payouts):
        # Add a space if num_entries is not an even number
        empty_entry = " " * 8
        num_entries = len(formatted_payouts)
        if num_entries % 2 != 0:
            formatted_payouts.append(empty_entry)
        return formatted_payouts

    def get_formatted_payouts(self) -> List[str]:
        # Format the card's sum : payout dictionary
        sums_to_payouts = self.card.payouts.items()
        formatted_payouts = []
        for sum, payout in sorted(sums_to_payouts):
            respaced_sum = self.respace_sum(str(sum))
            respaced_payout = self.respace_payout(str(payout))
            entry = DIVIDER.join([respaced_sum, respaced_payout])
            formatted_payouts.append(entry)
        return formatted_payouts

    def respace_sum(self, sum_value):
        chars_needed = '{:2}'
        return chars_needed.format(sum_value)

    def respace_payout(self, payout):
        chars_needed = '{:3}'
        return chars_needed.format(payout)