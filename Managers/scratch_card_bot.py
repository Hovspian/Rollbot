from GridGames.Parsers.line_parser import LineParser
from GridGames.ScratchCard.Hammerpot.hammerpot import Hammerpot
from GridGames.ScratchCard.scratch_card import ClassicScratchCard
from GridGames.input_error_handler import InputErrorHandler
from Managers.game_manager import GameManager


class ScratchCardBot(GameManager):
    # Handles user-game relationship for scratch cards / hammerpot
    def __init__(self, bot):
        super().__init__(bot)
        self.parser = LineParser(num_columns=3)
        self.error_handler = InputErrorHandler(bot)

    async def create_scratch_card(self, ctx):
        scratch_card = ClassicScratchCard()
        await self.initialize_game(scratch_card, ctx)
        return scratch_card

    async def create_hammerpot(self, ctx):
        hammerpot = Hammerpot()
        await self.initialize_game(hammerpot, ctx)
        return hammerpot

    async def initialize_game(self, game, ctx):
        game.initialize_card()
        game.host = ctx.message.author
        await self.say_starting_message(game)
        self.add_game(game)

    async def pick_line(self, game, raw_input):
        line = self.parser.get_line(raw_input)
        can_pick = await self.error_handler.check_can_pick_line(game)
        if line and can_pick:
            game.pick_line(line)
            await self.report_turn(game)

    async def say_starting_message(self, game):
        message = game.announcement.get_starting_message()
        await self.bot.say(message)

    async def next_turn(self, game, raw_input):
        formatted_parse = self.parser.get_formatted_parse(raw_input)
        validated_tiles = await self.error_handler.validate(game, formatted_parse)

        if validated_tiles:
            game.scratch_tiles(validated_tiles)
            await self.report_turn(game)

    async def report_turn(self, game):
        current_card = game.announcement.get_card()
        report = game.announcement.get_report()
        await self.bot.say(current_card)
        await self.bot.say(report)

    async def get_game(self, ctx):
        game = super().get_game(ctx)
        if game:
            return game
        else:
            await self.bot.say("You don't have an active card.")