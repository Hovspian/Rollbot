from GridGames.ScratchCard.constants import *
from typing import List


class CardRenderer:

    """
    Box drawing methods for grids.
    The game must implement properties: num_columns, num_rows and visible_grid.
    visible_grid can be filled using GridHandler.generate_grid().
    """

    def __init__(self, game):
        self.num_columns = game.num_columns  # int
        self.num_rows = game.num_rows  # int
        self.grid = game.visible_grid  # list[list[dict]]

    def render_card(self) -> str:
        rows = LINEBREAK.join(self.get_card_rows())
        card = [CODE_TAG, rows, CODE_TAG]
        return LINEBREAK.join(card)

    def get_card_rows(self) -> List[str]:
        column_header = self.__get_column_header()
        top_row_border = self.__draw_top_border()
        row_placeholders = self.__get_row_placeholders()
        card_rows = [column_header, top_row_border]

        def construct_grid(i, row):
            formatted_row = get_row(i, row)
            card_rows.append(formatted_row)
            card_rows.append(add_divider(i))

        def get_row(i, row):
            coordinate = ROW_LABELS[i]
            row_values = self.__get_emote_list(row)
            row_values.insert(0, coordinate)
            return row_placeholders.format(*row_values)

        def add_divider(i):
            is_last_row = i == self.num_rows - 1
            if is_last_row:
                return self.__draw_bottom_border()
            return self.__draw_column_divider()

        for i, row in enumerate(self.grid):
            construct_grid(i, row)

        return card_rows

    def __get_emote_list(self, symbols) -> List[str]:
        return [self.get_emote(symbol) for symbol in symbols]

    def __get_column_header(self) -> str:
        row_placeholders = self.__get_row_placeholders()
        column_labels = self.__get_column_labels()
        return row_placeholders.format(*column_labels)

    def __get_column_labels(self) -> List[str]:
        # Eg. ' ', 'A', 'B', 'C'
        column_labels = COLUMN_LABELS[:self.num_columns]
        column_labels.insert(0, SPACE)
        return column_labels

    def __get_row_placeholders(self) -> str:
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

    def __draw_top_border(self) -> str:
        # Eg.  ══╬═══╪═══╪═══╣
        cell_border = COLUMN_BORDER * 3
        cell = ''.join([cell_border, TOP_MIDDLE_INTERSECTION])
        last_cell = ''.join([cell_border, TOP_RIGHT_INTERSECTION])
        row = [COLUMN_BORDER * 2,
               TOP_LEFT_INTERSECTION,
               cell * (self.num_columns - 1),
               last_cell]
        return ''.join(row)

    def __draw_bottom_border(self) -> str:
        # Eg. ══╩═══╧═══╧═══╝
        cell_border = COLUMN_BORDER * 3
        cell = ''.join([cell_border, BOTTOM_MIDDLE_INTERSECTION])
        last_cell = ''.join([cell_border, BOTTOM_RIGHT_CORNER])
        row = [COLUMN_BORDER * 2,
               BOTTOM_LEFT_INTERSECTION,
               cell * (self.num_columns - 1),
               last_cell]
        return ''.join(row)

    def __draw_column_divider(self) -> str:
        # Eg. ──╫───┼───┼───╢
        cell_divider = COLUMN_DIVIDER * 3
        cell = ''.join([cell_divider, ROW_INTERSECTION])
        last_cell = ''.join([cell_divider, ROW_RIGHT_INTERSECTION])
        row = [COLUMN_DIVIDER * 2,
               ROW_LEFT_INTERSECTION,
               cell * (self.num_columns - 1),
               last_cell]
        return ''.join(row)

    @staticmethod
    def get_emote(symbol) -> str:
        # TODO not always an emote!
        return symbol['emote']