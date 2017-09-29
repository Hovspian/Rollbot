from GridGames.scratch_card import ScratchCard
from GridGames.coordinate_parser import CoordinateParser
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
        valid_parse = await self._validate(scratch_card, raw_input)
        if valid_parse:
            scratch_card.scratch_tiles(valid_parse)
            await self._report_turn(scratch_card)

    def check_game_end(self, ctx) -> bool:
        scratch_card = self.manager.get_game(ctx)
        if not scratch_card.in_progress:
            self.manager.remove_game(ctx)
            return True

    async def _report_turn(self, scratch_card):
        current_card = scratch_card.announcement.get_card()
        report = scratch_card.announcement.get_report()
        await self.bot.say(current_card)
        await self.bot.say(report)

    async def _validate(self, scratch_card, user_input):
        formatted_input = self.parser.format_input(user_input)
        valid_attempts = self.check_attempts(scratch_card, formatted_input)
        valid_input_tiles = self.check_input_tiles(formatted_input)
        valid_parse = self.parser.get_parse(formatted_input)

        if not valid_attempts:
            num_attempts = scratch_card.attempts_remaining
            await self._invalid_attempts_error(num_attempts)
        elif not valid_input_tiles or not valid_parse:
            await self._invalid_input_error()
        elif valid_parse:
            return valid_parse

    @staticmethod
    def check_attempts(scratch_card, formatted_input):
        valid_num_attempts = scratch_card.attempts_remaining
        if len(formatted_input) <= valid_num_attempts:
            return True

    @staticmethod
    def check_input_tiles(formatted_input):
        valid_num_coordinates = 2
        for message in formatted_input:
            if len(message) != valid_num_coordinates:
                return False
        return True

    async def _invalid_attempts_error(self, attempts):
        error = f'Please make up to {attempts} choices.'
        await self.bot.say(error)

    async def _invalid_input_error(self):
        await self.bot.say('Please input valid tiles. Eg: `/scratch A2`, `/scratch B1, C2`')


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
