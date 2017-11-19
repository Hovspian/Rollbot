from Core.helper_functions import *
from GridGames.Parsers.input_error_handler import InputErrorHandler
from GridGames.Parsers.line_parser import LineParser
from GridGames.ScratchCard.Hammerpot.hammerpot import Hammerpot
from GridGames.ScratchCard.scratch_card import ScratchCard
from Managers.GameManagers.game_manager import GameManager


class ScratchCardBot(GameManager):
    # Handles user-game relationship for scratch cards / hammerpot

    def __init__(self, bot, data_manager):
        super().__init__(bot)
        self.data_manager = data_manager
        self.parser = LineParser()
        self.error_handler = InputErrorHandler(bot)

    async def initialize_game(self, game):
        self.add_game(game)
        await self.say_starting_message(game)
        await self._set_game_end(game)

    async def make_action(self, ctx, action_to_perform: str) -> None:
        is_host = await self.check_game_host(ctx)
        game = await self.get_game(ctx)
        if is_host and game:
            raw_input = message_without_command(ctx.message.content)
            actions = {
                "scratch": self._attempt_scratch,
                "pick": self._attempt_pick_line
            }
            await actions[action_to_perform](game, raw_input)

    async def _attempt_scratch(self, game: ScratchCard, raw_input):
        validated_tiles = await self.error_handler.validate(game, raw_input)
        if validated_tiles:
            game.scratch_tiles(validated_tiles)
            await self.report_turn(game)

    async def _attempt_pick_line(self, game: Hammerpot, raw_input):
        line = self.parser.get_line(game, raw_input)
        can_pick = await self.error_handler.check_can_pick_line(game)
        if line and can_pick:
            game.pick_line(line)
            await self.report_turn(game)

    async def check_game_host(self, ctx) -> bool:
        game_host = await self.get_game_host(ctx)
        user = ctx.message.author
        if game_host == user:
            return True
        else:
            host_name = game_host.display_name
            await self.bot.say(f'The current game host is {host_name}. Please make a game in another channel.')

    async def get_game_host(self, ctx):
        game = await self.get_game(ctx)
        if game:
            return game.host

    async def say_starting_message(self, game):
        message = game.announcement.get_starting_message()
        await self.bot.say(message)

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