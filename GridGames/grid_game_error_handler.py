from GridGames.ScratchCard.constants import *
from typing import List


class GridErrorHandler:
    def __init__(self, bot):
        self.bot = bot
        self.ERROR_INVALID_INPUT = "Please input valid tiles within the board size. " \
                                   "Eg: `/scratch A2`, `/scratch B1, C2`"
        self.ERROR_INVALID_ATTEMPT = "Please make 1 choice."
        self.ERROR_INVALID_ATTEMPTS = "Please make up to {} choices."
        self.ERROR_REVEALED_TILE = "That tile has already been revealed."

    async def validate(self, game, parse) -> List[list]:
        return  await self.check_valid_parse(game, parse)

    async def check_valid_parse(self, game, parse) -> List[list]:
        valid_parse = self._strip_invalid_coordinates(parse)
        if valid_parse:
            return await self.check_usable_tiles(game, valid_parse)
        else:
            await self.bot.say(self.ERROR_INVALID_INPUT)

    async def check_usable_tiles(self, game, valid_parse) -> List[list]:
        valid_tiles = self._strip_occupied_tiles(game, valid_parse)
        if valid_tiles:
            return await self.check_valid_attempts(game, valid_tiles)
        else:
            await self.bot.say(self.ERROR_REVEALED_TILE)

    async def check_valid_attempts(self, game, valid_tiles) -> List[list]:
        valid_attempts = self._is_valid_attempts(game, valid_tiles)
        if valid_attempts:
            return valid_tiles
        else:
            await self._error_invalid_attempts(game.attempts_remaining)

    async def _error_invalid_attempts(self, attempts_remaining) -> None:

        if attempts_remaining > 1:
            error = self.ERROR_INVALID_ATTEMPTS.format(attempts_remaining)
        else:
            error = self.ERROR_INVALID_ATTEMPT
        await self.bot.say(error)

    @staticmethod
    def _strip_invalid_coordinates(parse):
        return [coordinates for coordinates in parse if coordinates is not None]

    def _strip_occupied_tiles(self, game, parse) -> List[list]:

        valid_coordinates = []

        def add_vacant_tile(coordinates):
            y = coordinates[0]
            x = coordinates[1]
            tile = game.card_grid[y][x]
            if self._is_vacant_tile(tile):
                valid_coordinates.append(coordinates)

        [add_vacant_tile(coordinates) for coordinates in parse]
        return valid_coordinates

    @staticmethod
    def _is_vacant_tile(tile) -> bool:
        return tile is NEUTRAL_TILE

    @staticmethod
    def _is_valid_attempts(game, valid_parse) -> bool:
        valid_num_attempts = game.attempts_remaining
        user_attempts = len(valid_parse)
        return user_attempts <= valid_num_attempts
