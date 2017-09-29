from GridGames.scratch_card import ScratchCard
from GridGames.coordinate_parser import CoordinateParser
from GridGames.constants import *
import asyncio


class ScratchCardBot:
    # Handles user-game relationship
    def __init__(self, bot):
        self.parser = CoordinateParser(num_columns=3)
        self.manager = GameManager(bot)
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
        validated = await self._validate(scratch_card, raw_input)
        if validated:
            scratch_card.scratch_tiles(validated)
            await self._report_turn(scratch_card)

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

    async def _validate(self, scratch_card, user_input):
        formatted_input = self.parser.format_input(user_input)
        valid_attempts = self.check_attempts(scratch_card, formatted_input)
        parse = self.parser.get_parse(formatted_input)
        valid_parse = self.remove_invalid_coordinates(parse)
        valid_tiles = self.remove_revealed_tiles(scratch_card, valid_parse)

        if not valid_attempts:
            num_attempts = scratch_card.attempts_remaining
            await self._error_invalid_attempts(num_attempts)
        elif not valid_parse:
            await self._error_invalid_input()
        elif not valid_tiles:
            await self._error_revealed_tile()
        else:
            return valid_tiles

    @staticmethod
    def remove_invalid_coordinates(parse):
        return [coordinates for coordinates in parse if coordinates is not None]

    @staticmethod
    def remove_revealed_tiles(scratch_card, parse):

        valid_coordinates = []

        def add_valid_tile(coordinates):
            y = coordinates[0]
            x = coordinates[1]
            tile = scratch_card.card_grid[y][x]
            if tile is neutral_tile:
                valid_coordinates.append(coordinates)

        [add_valid_tile(coordinates) for coordinates in parse]
        return valid_coordinates

    @staticmethod
    def check_attempts(scratch_card, formatted_input):
        valid_num_attempts = scratch_card.attempts_remaining
        if len(formatted_input) <= valid_num_attempts:
            return True

    @staticmethod
    def check_coordinate_length(formatted_input):
        valid_num_coordinates = 2
        for coordinates in formatted_input:
            if len(coordinates) != valid_num_coordinates:
                formatted_input.remove(coordinates)
        return formatted_input

    async def _error_invalid_attempts(self, attempts):
        error = f'Please make up to {attempts} choices.'
        await self.bot.say(error)

    async def _error_invalid_input(self):
        await self.bot.say('Please input valid tiles within the board-size. Eg: `/scratch A2`, `/scratch B1, C2`')

    async def _error_revealed_tile(self):
        await self.bot.say("That tile has already been revealed.")


class GameManager:
    # Manage ongoing games of a type
    def __init__(self, bot):
        self.bot = bot
        self.games_in_progress = {}

    def is_valid_new_game(self, host):
        return host not in self.games_in_progress

    async def invalid_game_error(self):
        await self.bot.say("Please finish your current game first.")

    def add_game(self, game):
        self.games_in_progress[game.host] = game

    def get_game(self, ctx):
        author = ctx.message.author
        if author in self.games_in_progress:
            return self.games_in_progress[author]

    def remove_game(self, ctx):
        author = ctx.message.author
        self.games_in_progress.pop(author)

    async def set_time_limit(self, game):
        host = game.host_name
        await asyncio.sleep(100.0)
        await self.bot.say(f"{host} has 20 seconds left!")
        await asyncio.sleep(20.0)
        await self.bot.say(f"Time limit elapsed. {host}'s game has ended.")
        self.games_in_progress.pop(game.host)
        return True
