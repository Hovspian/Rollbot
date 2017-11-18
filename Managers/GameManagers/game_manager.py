import asyncio
from constants import *


class GameManager:

    # Manage ongoing games of a type, including storage, add and removal.
    # Ie. users cannot create multiples of the same game before finishing their current one.

    def __init__(self, bot):
        self.bot = bot
        self.active_games = []

    def is_valid_user(self, host):
        # TODO not all games have registrants.
        is_in_game = self.get_user_game(host)
        return not is_in_game

    async def check_valid_user(self, host):
        if self.is_valid_user(host):
            return True
        else:
            await self.bot.say("Please finish your current game first.")

    def add_game(self, game):
        self.active_games.append(game)

    def get_game(self, ctx):
        user = ctx.message.author
        return self.get_user_game(user)

    def get_user_game(self, user):
        for game in self.active_games:
            for in_game_user in game.users:
                if in_game_user is user:
                    return game

    async def set_join_waiting_period(self, ctx):
        await self.say_setup_message(ctx)
        await asyncio.sleep(15)
        await self.say_last_call_message()
        await asyncio.sleep(5)

    async def say_last_call_message(self):
        await self.bot.say("Starting in 5 seconds. Last call to sign up.")

    async def say_setup_message(self, ctx):
        host_name = ctx.message.author.display_name
        setup_message = f"{host_name} is starting a game. Type /join in the next 20 seconds to join."
        await self.bot.say(setup_message)

    async def set_game_end(self, game):
        await TimeLimit(game, self.bot).set_time_limit()
        self._end_game(game)

    def _end_game(self, game):
        self.active_games.remove(game)


class TimeLimit:

    # Sets a time limit on the game session.
    # Games end when they are complete or time has run out.

    def __init__(self, game, bot):
        self.game = game
        self.bot = bot

    async def set_time_limit(self):
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
        host = self.game.host_name
        await self.bot.say(f"{host} has 1 minute left.")

    async def _low_time_warning(self):
        host = self.game.host_name
        await self.bot.say(f"{host} has 20 seconds left!")

    async def _time_out(self):
        host = self.game.host_name
        await self.bot.say(f"Time limit elapsed. {host}'s game has ended.")
        self.game.in_progress = False
