from GridGames.render_card import RenderCard
from GridGames.ScratchCard.constants import *
from typing import List


class RenderHammerpot(RenderCard):
    # Renders the payout table next to the card

    def __init__(self, card):
        super().__init__(card)
        self.payout_table = self._get_payout_table()

    def render_card(self) -> str:
        card = self.get_card_rows()
        combined_rows = []
        for i in range(len(card)):
            row = SPACER.join([card[i], self.payout_table[i]])
            combined_rows.append(row)
        combined_rows = LINEBREAK.join(combined_rows)
        return combined_rows

    def _get_payout_table(self) -> List[str]:
        # Number of rows should be equal to the scratch card
        rows = self._get_payout_rows()
        table_bottom = self._get_table_bottom(rows)
        table = [TABLE_HEADER, TABLE_WHITESPACE] + rows + table_bottom
        return table

    def _get_table_bottom(self, rows) -> List[str]:
        # Depending on the number of rows for sum : payout entries, expand the bottom of the table
        rows_needed = self.card.num_columns * 2 - len(rows)
        table_bottom = []
        for i in range(rows_needed):
            if i == rows_needed - 1:
                table_bottom.append(TABLE_BOTTOM)
            else:
                table_bottom.append(TABLE_WHITESPACE)
        return table_bottom

    def _get_payout_rows(self) -> List[str]:
        entries = self._get_payout_pairs()
        rows = []
        for entry in entries:
            payout_row = TABLE_PLACEHOLDER.format(*entry)
            rows.append(payout_row)
        return rows

    def _get_payout_pairs(self) -> List[List[dict]]:
        # A sum-payout entry has 8 characters, eg. 21 : 500
        formatted_payouts = self._get_formatted_payouts()
        entries = self._check_odd_num_entries(formatted_payouts)
        num_rows = len(formatted_payouts) // 2
        pairs = []

        for i in range(num_rows):
            start = 0 + i * 2
            end = 2 + i * 2
            pairs.append(entries[start:end])

        return pairs

    def _check_odd_num_entries(self, formatted_payouts) -> List[dict]:
        empty_entry = SPACE * 8
        num_entries = len(formatted_payouts)
        if not self._is_even_number(num_entries):
            # Add an 8-character space
            formatted_payouts.append(empty_entry)
        return formatted_payouts

    @staticmethod
    def _is_even_number(num_entries) -> bool:
        return num_entries % 2 == 0

    def _get_formatted_payouts(self) -> List[str]:
        # Format the card's sum : payout dictionary
        sums_to_payouts = self.card.payouts.items()
        formatted_payouts = []
        for sum, payout in sorted(sums_to_payouts):
            respaced_sum = self._respace_sum(str(sum))
            respaced_payout = self._respace_payout(str(payout))
            entry = DIVIDER.join([respaced_sum, respaced_payout])
            formatted_payouts.append(entry)
        return formatted_payouts

    def _respace_sum(self, sum_value) -> str:
        chars_needed = '{:2}'
        return chars_needed.format(sum_value)

    def _respace_payout(self, payout) -> str:
        chars_needed = '{:3}'
        return chars_needed.format(payout)