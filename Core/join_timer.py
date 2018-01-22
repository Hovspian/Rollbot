import asyncio

from Core.core_game_class import GameCore


class JoinTimer:
    def __init__(self, bot, game: GameCore):
        self.waiting = False
        self.join_time = 15
        self.bot = bot
        self.game = game
        self.host = game.host

    async def cancel_timer(self):
        self.waiting = False

    async def run(self) -> None:
        self.waiting = True
        until_five_seconds_left = self.join_time - 5
        while self.waiting:
            await self._say_setup_message()
            await asyncio.sleep(until_five_seconds_left)
            await self._say_last_call_message()
            await asyncio.sleep(5)
            await self._say_start_message()
            break

    async def _say_setup_message(self):
        host = self.game.host_name
        temp_message = await self.bot.say(f"{host} is starting a {self.game.title}. "
                                          f"Type `/join` in the next {self.join_time} seconds to join.")

    async def _say_last_call_message(self):
        temp_message = await self.bot.say("Last call to sign up.")

    async def _say_start_message(self):
        # TODO this triggers even if it fails the num players check
        pass
