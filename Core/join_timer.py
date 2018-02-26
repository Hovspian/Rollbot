import asyncio

from Core.core_game_class import GameCore


class JoinTimer:
    def __init__(self, bot, game: GameCore):
        self.join_time = 15
        self.counter = self.join_time
        self.bot = bot
        self.game = game
        self.host = game.host

    def cancel_timer(self):
        self.counter = 0

    async def run(self) -> None:
        while self.counter >= 0:
            await self.check_time_left()
            self.counter -= 1
            await asyncio.sleep(1)

    async def check_time_left(self):
        if self.counter == self.join_time:
            await self._say_setup_message()
        if self.counter == 5:
            await self._say_last_call_message()
        if self.counter == 0:
            await self._say_start_message()

    async def _say_setup_message(self):
        host = self.game.host_name
        await self.bot.say(f"{host} is starting a {self.game.title}. "
                           f"Type `/join` in the next {self.join_time} seconds to join.")

    async def _say_last_call_message(self):
        await self.bot.say("Last call to sign up!")

    async def _say_start_message(self):
        # TODO this triggers even if it fails the num players check
        pass
