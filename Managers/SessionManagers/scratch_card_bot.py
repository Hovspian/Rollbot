import asyncio
from Core.helper_functions import *
from Core.time_limit import TimeLimit
from GridGames.Parsers.input_error_handler import InputErrorHandler
from GridGames.Parsers.line_parser import LineParser
from GridGames.ScratchCard.Classic.classic_mode import ClassicScratchCard
from GridGames.ScratchCard.Hammerpot.hammerpot import Hammerpot
from GridGames.ScratchCard.scratch_card import ScratchCard
from Managers.SessionManagers.game_initializer import GameInitializer, SessionOptions


class ScratchCardBot:
    # Handles user-game relationship for scratch cards / hammerpot

    def __init__(self, options: SessionOptions):
        self.bot = options.bot
        self.classic_initializer = ScratchCardInitializer(options)
        self.hammerpot_initializer = HammerpotInitializer(options)
        self.move_handler = ScratchCardMoveHandler(options.bot, options.channel_manager)
        self.payout_handler = None

    async def create_classic(self, ctx):
        self.classic_initializer.initialize_game(ctx)

    async def create_hammerpot(self, ctx):
        self.hammerpot_initializer.initialize_game(ctx)

    async def scratch(self, ctx):
        self.move_handler.attempt_scratch(ctx)

    async def pick_line(self, ctx):
        self.move_handler.attempt_pick_line(ctx)


class ScratchCardInitializer(GameInitializer):
    def __init___(self, options: SessionOptions):
        super().__init__(options) #  TODO Doooo repeat yourself

    async def initialize_game(self, ctx):
        if await self._can_create_game(ctx):
            scratchcard = ClassicScratchCard(ctx)
            await self._create_session(scratchcard)

    async def _create_session(self, game: ScratchCard):
        self._add_game(game.ctx, game)
        await self._run_time_limit(game)
        self._remove_game(game.ctx)

    async def _run_time_limit(self, game):
        time_limit = TimeLimit(self.bot, game)
        await time_limit.run()

    async def say_starting_message(self, game):
        message = game.announcement.get_starting_message()
        await self.bot.say(message)


class HammerpotInitializer(GameInitializer):
    def __init___(self, options: SessionOptions):
        super().__init__(options)

    async def initialize_game(self, ctx):
        if await self._can_create_game(ctx):
            scratchcard = Hammerpot(ctx)
            await self._create_session(scratchcard)

    async def _create_session(self, game: ScratchCard):
        self._add_game(game.ctx, game)
        await self._run_time_limit(game)
        self._remove_game(game.ctx)

    async def _run_time_limit(self, game):
        time_limit = TimeLimit(self.bot, game)
        await time_limit.run()

    async def say_starting_message(self, game):
        message = game.announcement.get_starting_message()
        await self.bot.say(message)


class ScratchCardMoveHandler:
    def __init__(self, bot, channel_manager):
        self.bot = bot
        self.channel_manager = channel_manager
        self.error_handler = InputErrorHandler(bot)
        self.announcer = ScratchCardMoveAnnouncer(bot)
        self.parser = LineParser()

    async def attempt_scratch(self, ctx):
        if self._is_permitted_move(ctx):
            self._scratch(ctx)

    async def attempt_pick_line(self, ctx):
        if self._is_permitted_move(ctx):
            self._pick_line(ctx)

    async def _scratch(self, ctx):
        game = await self.get_game(ctx)
        coordinates = message_without_command(ctx.message.content)
        valid_tiles = await self.error_handler.validate_coordinates(game, coordinates)
        if valid_tiles:
            game.scratch_tiles(valid_tiles)
            await self.announcer.report_turn(game)

    async def _pick_line(self, ctx):
        game = await self.get_game(ctx)
        coordinates = message_without_command(ctx.message.content)  # TODO isn't there an API method for this?
        line = self.parser.get_line(game, coordinates)
        can_pick = await self.error_handler.check_can_pick_line(game)
        if line and can_pick:
            game.pick_line(line)
            await self.announcer.report_turn(game)

    async def _is_permitted_move(self, ctx):
        return await self.get_game(ctx) and await self._check_game_host(ctx)

    async def _check_game_host(self, ctx) -> bool:
        game_host = await self.get_game_host(ctx)
        user = ctx.message.author
        if game_host == user:
            return True
        else:
            await self.announcer.not_host_error(game_host)

    async def get_game_host(self, ctx):
        game = await self.get_game(ctx)
        return game.host

    async def get_game(self, ctx):
        game = self.channel_manager.get_game(ctx)
        if game:  # TODO and game matches ID
            return game
        else:
            await self.announcer.no_active_card_error()


class ScratchCardMoveAnnouncer:
    def __init__(self, bot):
        self.bot = bot
        self.messages = []  # TODO array to hold messages for cleanup

    async def report_turn(self, game):
        current_card = game.feedback.get_card()
        report = game.feedback.get_report()
        await self.bot.say(current_card)
        await self.bot.say(report)

    async def not_host_error(self, game_host):
        host_name = game_host.display_name
        temp_message = await self.bot.say(f'The current game host is {host_name}. '
                                          'Please make a game in another channel.')
        self._delay_delete_message(temp_message)

    async def no_active_card_error(self):
        temp_message = await self.bot.say("You don't have an active card.")
        self._delay_delete_message(temp_message)

    async def _delay_delete_message(self, message):
        await asyncio.sleep(5.0)
        await self.bot.delete_message(message)
