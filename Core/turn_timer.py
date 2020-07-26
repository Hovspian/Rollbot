import asyncio


class TurnTimer:
    """
    Puts a timer on player turns for multiplayer games.
    Multiplayer games must implement resolve_afk method to resolve AFKs.
    Runs while game is in_progress. When it ends, the channel will be vacated.
    """
    def __init__(self, bot, game):
        self.bot = bot
        self.game = game
        self.max_turn_time = 60  # Seconds
        self.low_time = 20
        self.time_left = self.max_turn_time

    async def run(self):
        while self.game.in_progress:
            await asyncio.sleep(1.0)
            if self.time_left == self.low_time:
                await self._low_time_warning()
            if self.time_left == 0:
                await self.check_afk()
                self.refresh_turn_timer()
            self.time_left -= 1

    def refresh_turn_timer(self):
        """
        When a player has made a move, the timer refreshes to max for the next person in line.
        """
        self.time_left = self.max_turn_time

    def set_low_time(self):
        """
        For reducing the amount of time on an AFKing player's subsequent turns.
        """
        self.time_left = self.low_time

    async def _low_time_warning(self):
        current_player = self.game.players[0]
        await self.game.ctx.send(f"{current_player.name} has 20 seconds.")

    async def check_afk(self):
        """
        The game decides what to do with an AFK player.
        """
        await self.game.resolve_afk()