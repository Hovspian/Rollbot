from typing import List

from Core.constants import GAME_ID
from Core.core_game_class import GameCore
from Core.helper_functions import message_without_command
from Core.join_timer import JoinTimer
from Core.time_limit import TimeLimit
from GridGames.Bombtile.bombtile import Bombtile
from GridGames.Parsers.coordinate_parser import CoordinateParser
from GridGames.Parsers.input_error_handler import InputErrorHandler
from GridGames.ScratchCard.constants import COLUMN_INPUTS, ROW_INPUTS, EMPTY_TILE
from GridGames.grid import GridHandler
from Managers.SessionManagers.game_initializer import GameInitializer, SessionOptions


class BombtileBot:

    """
    A session manager for Bombtile. Connects user commands with the respective functionality.
    """

    def __init__(self, options: SessionOptions):
        self.initializer = BombtileInitializer(options)
        self.channel_manager = options.channel_manager
        self.bot = options.bot
        self.move_handler = BombtileMoveHandler(options.bot, options.channel_manager)

    async def create_bombtile(self, ctx):
        await self.initializer.initialize_game(ctx)

    async def flip(self, ctx):
        await self.move_handler.attempt_flip(ctx)


class BombtileInitializer(GameInitializer):

    """
    Create instances of Bombtile.
    """

    def __init__(self, options):
        super().__init__(options)

    async def initialize_game(self, ctx):
        if await super()._can_create_game(ctx):
            bombtile = Bombtile(ctx, self.bot)
            await self._create_session(bombtile)

    async def _create_session(self, bombtile: Bombtile):
        self._add_game(bombtile.ctx, bombtile)
        await self._run_join_timer(bombtile)
        await bombtile.run()
        self._remove_game(bombtile.ctx)
        self.data_manager.batch_transfer(bombtile.get_payouts())

    async def _run_join_timer(self, game):
        join_timer = JoinTimer(self.bot, game)
        await self.channel_manager.add_join_timer(game.host, join_timer)


class BombtileMoveHandler:

    """
    Makes sure the player move is legal within the rules of the game.
    """

    def __init__(self, bot, channel_manager):
        self.bot = bot
        self.channel_manager = channel_manager

    async def attempt_flip(self, ctx) -> None:
        error = self._get_move_error(ctx)
        if error:
            await ctx.send(error)
            return
        await self._flip(ctx)

    async def _flip(self, ctx) -> None:
        game = self._get_game(ctx)
        input_handler = BombtileInputValidator(self.bot, game)
        valid_tile = await input_handler.validate_input(ctx)
        if valid_tile:
            await game.flip(valid_tile)

    def _get_move_error(self, ctx) -> str or None:
        game = self._get_game(ctx)
        user = ctx.message.author
        if not game:
            return "No game in this channel."
        if not game.in_progress:
            return "The game hasn't started yet."
        if not game.is_turn(user):
            return "It's not your turn. Please wait."
        return None

    def _get_game(self, ctx) -> Bombtile or None:
        user = ctx.message.author
        channel = ctx.message.channel
        game = self.channel_manager.get_game(channel)
        if game and self._is_in_game(game, user):
            return game

    @staticmethod
    def _is_in_game(game, user) -> bool:
        return any(in_game_user for in_game_user in game.users if in_game_user is user)

    @staticmethod
    async def _is_matching_game(game: GameCore) -> bool:
        return game.id == GAME_ID["BOMBTILE"]


class BombtileInputValidator:

    """
    Makes sure the user's input creates valid coordinates.
    """

    def __init__(self, bot, game: Bombtile):
        self.bot = bot
        self.game = game
        self.num_columns = game.num_columns
        self.num_rows = game.num_rows
        self.parser = CoordinateParser()

    async def validate_input(self, ctx):
        raw_input = message_without_command(ctx.message.content)
        formatted_input = self.parser.format_input(raw_input)
        is_in_bounds = await self._check_in_bounds(formatted_input[0], ctx)
        if is_in_bounds:
            return await self._get_parsed_coordinates(formatted_input, ctx)

    async def _get_parsed_coordinates(self, formatted_input, ctx):
        coordinates = self.parser.get_single_parse(formatted_input)
        if await self._check_unflipped_tile(coordinates, ctx):
            return coordinates

    async def _check_unflipped_tile(self, list_coordinates: List[int], ctx) -> bool:
        if self.game.is_flippable_tile(list_coordinates):
            return True
        await ctx.send("That tile has already been flipped.")

    async def _check_in_bounds(self, coordinates: str, ctx):
        if self._valid_num_axes(coordinates) and self._is_in_bounds(coordinates):
            return True
        await ctx.send("Please flip a valid tile within the board size. Eg. `/flip A0`")

    @staticmethod
    def _valid_num_axes(coordinates: str) -> bool:
        # x, y only
        return len(coordinates) == 2

    def _is_in_bounds(self, coordinates: str) -> bool:
        # Eg. accepts ['a', '2']
        x = False
        y = False
        for coordinate in coordinates:
            if coordinate in COLUMN_INPUTS[:self.num_columns]:
                y = True
            elif coordinate in ROW_INPUTS[:self.num_rows]:
                x = True
        return x and y
