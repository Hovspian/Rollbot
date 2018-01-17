import asyncio
from Core.core_game_class import GameCore


class TimeLimit:

    # Sets a time limit on the game session.
    # Games end when they are complete or time has run out.

    def __init__(self, bot, game):
        self.bot = bot
        self.game = game

    async def run(self):
        time_left = self.game.max_time_left

        while self.game.in_progress:
            await asyncio.sleep(1.0)
            time_left -= 1
            if time_left == 60:
                await self._medium_time_warning()
            if time_left == 20:
                await self._low_time_warning()
            if time_left == 0:
                await self._time_out()
                break

    async def _medium_time_warning(self):
        host = self.game.get_host_name()
        await self.bot.say(f"{host} has 1 minute left.")

    async def _low_time_warning(self):
        host = self.game.get_host_name()
        await self.bot.say(f"{host} has 20 seconds left!")

    async def _time_out(self):
        host = self.game.get_host_name()
        await self.bot.say(f"Time limit elapsed. {host}'s game has ended.")
        self.game.end_game()