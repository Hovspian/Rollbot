from Managers.game_manager import GameManager
from helper_functions import *
import asyncio
from HammerRace.hammer_modes import *


class HammerRaceBot(GameManager):
    def __init__(self, bot):
        super().__init__(bot)

    async def setup_race(self, hammer_race):
        if hammer_race.valid_num_participants():
            await self.run_race(hammer_race)
            await self.bot.say(hammer_race.winner_report())
        else:
            await self.bot.say(hammer_race.invalid_participants_error)

    async def run_race(self, hammer_race):
        hammer_race.in_progress = True
        await self.bot.say(hammer_race.round_report())

        while hammer_race.in_progress:
            await asyncio.sleep(2.0)
            hammer_race.next_round()
            await self.bot.say(hammer_race.round_report())
