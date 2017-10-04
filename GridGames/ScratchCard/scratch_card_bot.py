from GridGames.ScratchCard.scratch_card import ScratchCard
from GridGames.coordinate_parser import CoordinateParser
from GridGames.grid_game_error_handler import GridErrorHandler
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
        formatted_parse = self.parser.get_formatted_parse(raw_input)
        validated_tiles = await self.error_handler.validate(scratch_card, formatted_parse)

        if validated_tiles:
            scratch_card.scratch_tiles(validated_tiles)
            await self._report_turn(scratch_card)

    def check_game_end(self, ctx):
        scratch_card = self.manager.get_game(ctx)
        if not scratch_card.in_progress:
            self.manager.remove_game(ctx)

    async def _report_turn(self, scratch_card):
        current_card = scratch_card.announcement.get_card()
        report = scratch_card.announcement.get_report()
        await self.bot.say(current_card)
        await self.bot.say(report)
