from GridGames.ScratchCard.constants import *
from GridGames.Parsers.line_parser import CoordinateParser
from typing import List

ERROR = {"INVALID_INPUT": "Please input valid tiles within the board size. Eg: `/scratch A2`, `/scratch B1, C2`",
         "INVALID ATTEMPT": "Please make 1 choice.",
         "INVALID ATTEMPTS": "Please make up to {} choices.",
         "TILE_REVEALED": "That tile has already been used.",
         "TILES_TO_REVEAL": "Please finish revealing your tiles first.",
         "NO_ATTEMPTS": "You've revealed all the available tiles. Please `/pick` a column, row, or diagonal.",
         "INCORRECT_GAME_COMMAND": "That command is for another kind of game."}


class InputErrorHandler:
    def __init__(self, bot):
        self.bot = bot
        self.parser = CoordinateParser()

    async def validate_coordinates(self, game, raw_input) -> List[str]:
        formatted_input = self.parser.format_input(raw_input)
        valid_entries = await self._initial_validate(game, formatted_input)
        if valid_entries:
            parsed = self.parser.get_parse(valid_entries)
            valid_tiles = await self._secondary_validate(game, parsed)
            return valid_tiles

    async def _initial_validate(self, game, formatted_input):
        initial_validator = InitialFilter(game, formatted_input)
        valid_entries = await self._run_validator(initial_validator)
        await self._check_ignored_warning(initial_validator)
        return valid_entries

    async def _secondary_validate(self, game, parsed_input):
        secondary_validator = SecondaryFilter(game, parsed_input)
        valid_entries = await self._run_validator(secondary_validator)
        return valid_entries

    async def _run_validator(self, validator):
        validator.run_filter()

        if validator.error:
            await self.bot.say(validator.error)
        else:
            return validator.valid_entries

    async def _check_ignored_warning(self, validator):
        # Outputs invalid entries from running the filter
        if validator.ignored_entries:
            invalid_entries = ", ".join(validator.ignored_entries)
            skip_message = SPACE.join(["Skipped invalid:", invalid_entries])
            await self.bot.say(skip_message)

    async def check_can_pick_line(self, game) -> bool:
        error = self.check_line_error(game)
        if error:
            await self.bot.say(error)
        else:
            return True

    @staticmethod
    def check_line_error(game):
        error = False
        if not hasattr(game, "pick_line"):
            error = ERROR["INCORRECT_GAME_COMMAND"]
        elif game.attempts_remaining > 0:
            error = ERROR["TILES_TO_REVEAL"]
        return error

    @staticmethod
    def split_input(message) -> str:
        return message.split(',')


class InitialFilter:
    # Filters the user input List[str], separating valid_entries and ignored_entries (invalid entries)
    # Stops running when the input is unusable (error is no longer None).

    def __init__(self, grid_game, user_input):
        self.grid_game = grid_game
        self.num_columns = self.grid_game.num_columns
        self.valid_entries = user_input
        self.ignored_entries = []
        self.error = None

    def run_filter(self) -> None:
        while self.error is None:
            self._check_valid_num_coordinates()
            self._check_in_bounds()
            self._check_valid_attempts()
            break

    def _check_valid_attempts(self):
        valid_attempts = self._is_valid_attempts()
        if not valid_attempts:
            self._error_invalid_attempts()

    def _check_valid_num_coordinates(self):

        def sort_by_size(coordinates):
            valid_num_coordinates = 2
            if len(coordinates) == valid_num_coordinates:
                return coordinates
            self.ignored_entries.append(coordinates)

        self.valid_entries = list(filter(sort_by_size, self.valid_entries))
        if not self.valid_entries:
            self.error = ERROR["INVALID_INPUT"]

    def _check_in_bounds(self):

        def filter_valid(coordinates):
            if self._is_in_bounds(coordinates):
                return coordinates
            else:
                self.ignored_entries.append(coordinates)

        self.valid_entries = list(filter(filter_valid, self.valid_entries))
        if not self.valid_entries:
            self.error = ERROR["INVALID_INPUT"]

    def _is_in_bounds(self, coordinates) -> bool:
        x = False
        y = False
        for coordinate in coordinates:
            if coordinate in COLUMN_INPUTS[:self.num_columns]:
                y = True
            elif coordinate in ROW_INPUTS[:self.num_columns]:
                x = True
        return x and y

    def _error_invalid_attempts(self) -> None:
        num_attempts = self.grid_game.attempts_remaining
        if num_attempts == 0:
            self.error = ERROR["NO_ATTEMPTS"]
        elif num_attempts > 1:
            self.error = ERROR["INVALID ATTEMPTS"].format(num_attempts)
        else:
            self.error = ERROR["INVALID ATTEMPT"]

    def _is_valid_attempts(self) -> bool:
        user_attempts = len(self.valid_entries)
        return user_attempts <= self.grid_game.attempts_remaining


class SecondaryFilter:
    # Takes parsed coordinates and filters occupied tiles
    def __init__(self, grid_game, parsed_input):
        self.grid_game = grid_game
        self.valid_entries = parsed_input
        self.ignored_entries = []
        self.error = None

    def run_filter(self) -> None:
        while self.error is None:
            self.filter_usable_tiles()
            break

    def filter_usable_tiles(self):
        # Remove non-neutral tiles, eg. if they've already been revealed

        def check_vacant_tile(coordinates):
            y = coordinates[0]
            x = coordinates[1]
            tile = self.grid_game.card_grid[y][x]
            if self._is_vacant_tile(tile):
                return coordinates
            else:
                self.ignored_entries.append(coordinates)

        self.valid_entries = list(filter(check_vacant_tile, self.valid_entries))
        if not self.valid_entries:
            self.error = (ERROR["TILE_REVEALED"])

    @staticmethod
    def _is_vacant_tile(tile) -> bool:
        return tile is NEUTRAL_TILE
