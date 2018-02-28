from GridGames.ScratchCard.constants import *
from typing import List


class CardRenderer:
    # Box drawing methods for grid

    def __init__(self, game):
        self.num_columns = game.num_columns
        self.num_rows = game.num_rows
        self.card_grid = game.card_grid

    def render_card(self) -> str:
        rows = LINEBREAK.join(self.get_card_rows())
        card = [CODE_TAG, rows, CODE_TAG]
        return LINEBREAK.join(card)

    def get_card_rows(self) -> List[str]:
        column_header = self.get_column_header()
        top_row_border = self.draw_top_border()
        row_placeholders = self.get_row_placeholders()
        card_rows = [column_header, top_row_border]

        def construct_grid(i, row):
            formatted_row = get_row(i, row)
            card_rows.append(formatted_row)
            card_rows.append(add_divider(i))

        def get_row(i, row):
            coordinate = ROW_LABELS[i]
            row_values = self.get_emote_list(row)
            row_values.insert(0, coordinate)
            return row_placeholders.format(*row_values)

        def add_divider(i):
            if is_last_row(i):
                return self.draw_bottom_border()
            return self.draw_column_divider()

        def is_last_row(i):
            return i == self.num_rows - 1

        [construct_grid(i, row) for i, row in enumerate(self.card_grid)]
        return card_rows

    def get_emote_list(self, symbols) -> List[str]:
        return [self.get_emote(symbol) for symbol in symbols]

    @staticmethod
    def get_emote(symbol):
        return symbol['emote']

    def get_column_header(self):
        row_placeholders = self.get_row_placeholders()
        column_labels = self.get_column_labels()
        return row_placeholders.format(*column_labels)

    def get_column_labels(self):
        # Eg. ' ', 'A', 'B', 'C'
        column_labels = COLUMN_LABELS[:self.num_columns]
        column_labels.insert(0, SPACE)
        return column_labels

    def get_row_placeholders(self):
        # Eg. {} ║ {} │ {} │ {} ║
        placeholder = '{}'
        cell = ''.join([placeholder, ROW_DIVIDER])
        last_cell = ''.join([placeholder, ROW_BORDER])
        row = [placeholder,
               SPACE,
               ROW_BORDER,
               cell * (self.num_columns - 1),
               last_cell]
        return ''.join(row)

    def draw_top_border(self):
        # Eg.  ══╬═══╪═══╪═══╣
        cell_border = COLUMN_BORDER * 3
        cell = ''.join([cell_border, TOP_MIDDLE_INTERSECTION])
        last_cell = ''.join([cell_border, TOP_RIGHT_INTERSECTION])
        row = [COLUMN_BORDER * 2,
               TOP_LEFT_INTERSECTION,
               cell * (self.num_columns - 1),
               last_cell]
        return ''.join(row)

    def draw_bottom_border(self):
        # Eg. ══╩═══╧═══╧═══╝
        cell_border = COLUMN_BORDER * 3
        cell = ''.join([cell_border, BOTTOM_MIDDLE_INTERSECTION])
        last_cell = ''.join([cell_border, BOTTOM_RIGHT_CORNER])
        row = [COLUMN_BORDER * 2,
               BOTTOM_LEFT_INTERSECTION,
               cell * (self.num_columns - 1),
               last_cell]
        return ''.join(row)

    def draw_column_divider(self):
        # Eg. ──╫───┼───┼───╢
        cell_divider = COLUMN_DIVIDER * 3
        cell = ''.join([cell_divider, ROW_INTERSECTION])
        last_cell = ''.join([cell_divider, ROW_RIGHT_INTERSECTION])
        row = [COLUMN_DIVIDER * 2,
               ROW_LEFT_INTERSECTION,
               cell * (self.num_columns - 1),
               last_cell]
        return ''.join(row)