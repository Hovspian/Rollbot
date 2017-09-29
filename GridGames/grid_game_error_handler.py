from GridGames.ScratchCard.constants import *


class GridErrorHandler:
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def remove_invalid_coordinates(parse):
        return [coordinates for coordinates in parse if coordinates is not None]

    async def validate(self, game, parse):
        valid_parse = self.remove_invalid_coordinates(parse)

        if not valid_parse:
            await self._error_invalid_input()
            return

        valid_tiles = self.remove_revealed_tiles(game, valid_parse)
        if not valid_tiles:
            await self._error_revealed_tile()
            return

        valid_attempts = self.check_attempts(game, valid_tiles)
        if not valid_attempts:
            num_attempts = game.attempts_remaining
            await self._error_invalid_attempts(num_attempts)
            return

        return valid_tiles

    @staticmethod
    def remove_revealed_tiles(game, parse):

        valid_coordinates = []

        def add_valid_tile(coordinates):
            y = coordinates[0]
            x = coordinates[1]
            tile = game.card_grid[y][x]
            if tile is NEUTRAL_TILE:
                valid_coordinates.append(coordinates)

        [add_valid_tile(coordinates) for coordinates in parse]
        return valid_coordinates

    @staticmethod
    def check_attempts(game, formatted_input):
        valid_num_attempts = game.attempts_remaining
        if len(formatted_input) <= valid_num_attempts:
            return True

    async def _error_invalid_attempts(self, attempts):
        if attempts > 1:
            error = f'Please make up to {attempts} choices.'
        else:
            error = f'Please make up to {attempts} choice.'
        await self.bot.say(error)

    async def _error_invalid_input(self):
        await self.bot.say('Please input valid tiles within the board size. Eg: `/scratch A2`, `/scratch B1, C2`')

    async def _error_revealed_tile(self):
        await self.bot.say("That tile has already been revealed.")