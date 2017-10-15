import asyncio
from HammerRace.hammer_modes import *
from Managers.GameManagers.game_manager import GameManager


class HammerRaceBot(GameManager):
    def __init__(self, bot):
        super().__init__(bot)

    def initialize_game(self, game):
        self.add_game(game)

    def create_askhammer(self, ctx):
        hammer_race = ClassicHammer(ctx)
        self.initialize_game(hammer_race)
        return hammer_race

    def create_comparisonhammer(self, ctx):
        hammer_race = ComparisonHammer(ctx)
        self.initialize_game(hammer_race)
        return hammer_race

    def create_versushammer(self, ctx):
        hammer_race = VersusHammer(ctx)
        self.initialize_game(hammer_race)
        return hammer_race

    async def say_start_message(self, hammer_race):
        start_message = hammer_race.get_start_message()
        if start_message:
            await self.bot.say(start_message)

    async def start_race(self, hammer_race):
        if hammer_race.valid_num_participants():
            await self.say_start_message(hammer_race)
            await self.run_race(hammer_race)
        else:
            await self.bot.say(hammer_race.invalid_participants_error)

    async def run_race(self, hammer_race):
        hammer_race.in_progress = True
        await self.bot.say(hammer_race.round_report())

        while hammer_race.in_progress:
            await asyncio.sleep(2.0)
            hammer_race.next_round()
            await self.bot.say(hammer_race.round_report())

        await self.bot.say(hammer_race.winner_report())

    async def say_setup_message(self, ctx):
        host_name = ctx.message.author.display_name
        setup_message = self._get_setup_message(host_name, game_name="a race")
        await self.bot.say(setup_message)
