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
        self._end_wait()

    async def run(self) -> None:
        self.waiting = True
        while self.waiting:
            await self._say_setup_message()
            await asyncio.sleep(self.join_time - 5)
            await self._say_last_call_message()
            await asyncio.sleep(5)
            break

    async def _end_wait(self) -> None:
        self.waiting = False

    async def _say_setup_message(self):
        host = self.game.host_name
        temp_message = await self.bot.say(f"{host} is starting a {self.game.title}."
                                     f"Type `/join` in the next {self.join_time} seconds to join.")
        self._auto_delete_message(temp_message)

    async def _say_last_call_message(self):
        temp_message = await self.bot.say("Last chance to sign up!")
        self._auto_delete_message(temp_message)

    async def _say_start_message(self):
        pass

    async def _auto_delete_message(self, message):
        await asyncio.sleep(5.0)
        await self.bot.delete_message(message)
