import asyncio

from Core.join_timer import JoinTimer
from HammerRace.hammer_modes import *
from Managers.SessionManagers.game_initializer import GameInitializer, SessionOptions
from Managers.remote_data_manager import RemoteDataManager


class HammerRaceBot:
    def __init__(self, options: SessionOptions):
        self.channel_manager = options.channel_manager
        self.bot = options.bot
        self.classic_initializer = ClassicRaceInitializer(options)
        self.comparison_initializer = ComparisonInitializer(options)
        self.versus_initializer = VersusHammerInitializer(options)
        # self.payout_handler = HammerPayoutHandler()

    async def create_classic_race(self, ctx):
        await self.classic_initializer.initialize_game(ctx)

    async def create_comparison(self, ctx):
        await self.comparison_initializer.initialize_game(ctx)

    async def create_versus(self, ctx):
        await self.versus_initializer.initialize_game(ctx)
        # TODO sort payouts


class ClassicRaceInitializer(GameInitializer):

    def __init__(self, options: SessionOptions):
        super().__init__(options)

    async def initialize_game(self, ctx):
        if await self._can_create_game(ctx):
            race = ClassicHammer(self.bot, ctx)
            await self._create_session(race)

    async def _create_session(self, race: HammerRace):
        self._add_game(race.ctx, race)
        await race.run()
        self._remove_game(race.ctx)


class ComparisonInitializer(GameInitializer):

    def __init__(self, options: SessionOptions):
        super().__init__(options)

    async def initialize_game(self, ctx):
        if await self._can_create_game(ctx):
            race = ComparisonHammer(self.bot, ctx)
            await self._create_session(race)

    async def _create_session(self, race: HammerRace):
        self._add_game(race.ctx, race)
        await race.run()
        self._remove_game(race.ctx)


class VersusHammerInitializer(GameInitializer):
    def __init__(self, options: SessionOptions):
        super().__init__(options)

    async def initialize_game(self, ctx):
        if await self._can_create_game(ctx):
            race = VersusHammer(self.bot, ctx)
            await self._create_session(race)
            self.data_manager.batch_transfer(race.payouts)

    async def _create_session(self, race: HammerRace):
        self._add_game(race.ctx, race)
        await self._run_join_timer(race)
        await race.run()
        self._remove_game(race.ctx)

    async def _run_join_timer(self, race: HammerRace):
        timer = JoinTimer(self.bot, race)
        await self.channel_manager.add_join_timer(race.host, timer)
