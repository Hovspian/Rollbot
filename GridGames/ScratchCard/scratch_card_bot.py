from GridGames.ScratchCard.constants import *
from GridGames.ScratchCard.scratch_card import ScratchCard
from GridGames.coordinate_parser import CoordinateParser
from Managers.game_manager import GameManager


class ScratchCardBot:
    # Handles user-game relationship
    def __init__(self, bot):
        self.parser = CoordinateParser(num_columns=3)
        self.manager = GameManager(bot)
        self.error_handler = GridErrorHandler(bot)
        self.bot = bot

    def create_scratch_card(self, ctx):
        scratch_card = ScratchCard()
        scratch_card.host = ctx.message.author
        self.manager.add_game(scratch_card)
        return scratch_card

    async def starting_message(self, scratch_card):
        message = scratch_card.announcement.get_starting_message()
        await self.bot.say(message)

    async def next_turn(self, scratch_card, raw_input):
        formatted_parse = self.get_formatted_parse(raw_input)
        validated = await self.error_handler.validate(scratch_card, formatted_parse)
        if validated:
            scratch_card.scratch_tiles(validated)
            await self._report_turn(scratch_card)

    async def get_formatted_parse(self, raw_input):
        formatted_input = self.parser.format_input(raw_input)
        return self.parser.get_parse(formatted_input)

    async def _report_turn(self, scratch_card):
        current_card = scratch_card.announcement.get_card()
        report = scratch_card.announcement.get_report()
        await self.bot.say(current_card)
        await self.bot.say(report)

    def check_game_end(self, ctx) -> bool:
        scratch_card = self.manager.get_game(ctx)
        if not scratch_card.in_progress:
            self.manager.remove_game(ctx)
            return True


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