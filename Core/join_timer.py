import asyncio


class JoinTimer:

    def __init__(self):
        self.waiting = False
        self.join_time = 15

    async def cancel_wait(self):
        self.end_wait()

    async def set_join_waiting_period(self) -> None:
        self.waiting = True
        while self.waiting:
            await self._say_setup_message()
            await asyncio.sleep(self.join_time - 5)
            await self._say_last_call_message()
            await asyncio.sleep(5)
            break

    async def end_wait(self) -> None:
        self.waiting = False

    async def _say_last_call_message(self):
        pass

    async def _say_setup_message(self):
        pass

    async def _say_start_message(self):
        pass
