from Core.time_limit import TimeLimit
from Managers.SessionManagers.game_initializer import SessionOptions, GameInitializer
from RollGames.join_timer import NormalRollJoinTimer, DifferenceRollJoinTimer, CountdownRollJoinTimer
from RollGames.roll_game_modes import *


class RollGameBot:

    def __init__(self, options: SessionOptions):
        self.bot = options.bot
        self.normal_initializer = NormalRollInitializer(options)
        self.difference_initializer = DifferenceRollInitializer(options)
        self.countdown_initializer = CountdownRollInitializer(options)
        self.move_handler = None

    async def create_normal_roll(self, ctx, bet):
        await self.normal_initializer.initialize_game(ctx, bet)

    async def create_difference_roll(self, ctx, bet):
        await self.difference_initializer.initialize_game(ctx, bet)

    async def create_countdown_roll(self, ctx, bet):
        await self.countdown_initializer.initialize_game(ctx, bet)


class RollGameInitializer(GameInitializer):

    def __init__(self, options):
        super().__init__(options)

    async def initialize_game(self, ctx, *bet):
        if await self._can_create_game(ctx):
            game = self.get_game_to_create()
            initialized = game(self.bot, ctx, bet)
            await self._create_session(initialized)

    async def _create_session(self, game: RollGame):
        self._add_game(game.ctx, game)
        await self._run_join_timer(game)
        await game.start_rolls()
        await self._run_time_limit(game)
        self._remove_game(game.ctx)

    async def _run_time_limit(self, game):
        time_limit = TimeLimit(self.bot, game)
        await time_limit.run()

    @abstractmethod
    async def _run_join_timer(self, game):
        raise NotImplementedError

    @abstractmethod
    def get_game_to_create(self):
        raise NotImplementedError


class NormalRollInitializer(RollGameInitializer):

    def __init__(self, options):
        super().__init__(options)

    def get_game_to_create(self):
        return NormalRollGame

    async def _run_join_timer(self, game):
        timer = NormalRollJoinTimer(self.bot, game)
        await self.channel_manager.add_join_timer(game.host, timer)


class DifferenceRollInitializer(RollGameInitializer):

    def __init__(self, options):
        super().__init__(options)

    def get_game_to_create(self):
        return DifferenceRollGame

    async def _run_join_timer(self, game):
        timer = DifferenceRollJoinTimer(self.bot, game)
        await self.channel_manager.add_join_timer(game.host, timer)


class CountdownRollInitializer(RollGameInitializer):

    def __init__(self, options):
        super().__init__(options)

    def get_game_to_create(self):
        return CountdownRollGame

    async def _run_join_timer(self, game):
        timer = CountdownRollJoinTimer(self.bot, game)
        await self.channel_manager.add_join_timer(game.host, timer)