import asyncio

from Core.constants import GAME_ID
from Core.core_game_class import GameCore
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
        self.classic_initializer = ClassicScratchInitializer(options)
        self.hammerpot_initializer = HammerpotInitializer(options)
        self.move_handler = ScratchCardMoveHandler(options.bot, options.channel_manager)
        self.payout_handler = None

    async def create_classic(self, ctx):
        await self.classic_initializer.initialize_game(ctx)

    async def create_hammerpot(self, ctx):
        await self.hammerpot_initializer.initialize_game(ctx)

    async def scratch(self, ctx):
        await self.move_handler.attempt_scratch(ctx)

    async def pick_line(self, ctx):
        await self.move_handler.attempt_pick_line(ctx)


class ScratchCardInitializer(GameInitializer):
    def __init___(self, options: SessionOptions):
        super().__init__(options)

    async def _create_session(self, game: ScratchCard):
        self._add_game(game.ctx, game)
        await self.say_starting_message(game)
        await self._run_time_limit(game)
        self._remove_game(game.ctx)
        self._save_payout(game)

    async def _run_time_limit(self, game):
        time_limit = TimeLimit(self.bot, game)
        await time_limit.run()

    async def say_starting_message(self, game):
        message = game.feedback.announce_start()
        await self.bot.say(message)

    def _save_payout(self, game):
        to_user = game.get_host()
        gold_amount = game.get_payout()
        if gold_amount != 0:
            from_rollbot = self.bot.user
            self.data_manager.single_transfer(to_user, gold_amount, from_rollbot)


class ClassicScratchInitializer(ScratchCardInitializer):
    def __init___(self, options: SessionOptions):
        super().__init__(options)

    async def initialize_game(self, ctx):
        if await self._can_create_game(ctx):
            scratchcard = ClassicScratchCard(ctx)
            await self._create_session(scratchcard)


class HammerpotInitializer(ScratchCardInitializer):
    def __init___(self, options: SessionOptions):
        super().__init__(options)

    async def initialize_game(self, ctx):
        if await self._can_create_game(ctx):
            scratchcard = Hammerpot(ctx)
            await self._create_session(scratchcard)


class ScratchCardMoveHandler:
    def __init__(self, bot, channel_manager):
        self.bot = bot
        self.channel_manager = channel_manager
        self.error_handler = InputErrorHandler(bot)
        self.announcer = ScratchCardMoveAnnouncer(bot)
        self.parser = LineParser()

    async def attempt_scratch(self, ctx):
        if await self._is_permitted_move(ctx):
            await self._scratch(ctx)

    async def attempt_pick_line(self, ctx):
        if await self._is_permitted_move(ctx) and await self._is_pick_valid(ctx):
            await self._pick_line(ctx)

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
        game = await self.get_game(ctx)
        return game and await self._check_game_host(ctx)

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
        channel = ctx.message.channel
        game = self.channel_manager.get_game(channel)
        if game and await self._is_matching_game(game):
            return game
        else:
            await self.announcer.no_active_card_error()

    # Only Hammerpot uses /pick so far.
    async def _is_pick_valid(self, ctx) -> bool:
        game = await self.get_game(ctx)
        if game.id == GAME_ID["HAMMERPOT"]:
            return True
        else:
            await self.announcer.wrong_game_error()

    @staticmethod
    async def _is_matching_game(game: GameCore):
        return game.id == GAME_ID["SCRATCHCARD"] or game.id == GAME_ID["HAMMERPOT"]


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
        await self._auto_delete_message(temp_message)

    async def no_active_card_error(self):
        temp_message = await self.bot.say("You don't have an active card.")
        await self._auto_delete_message(temp_message)

    async def wrong_game_error(self):
        temp_message = await self.bot.say("That command is for another game.")
        await self._auto_delete_message(temp_message)

    async def _auto_delete_message(self, message):
        await asyncio.sleep(5.0)
        await self.bot.delete_message(message)
