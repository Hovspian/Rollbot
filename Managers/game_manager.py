import asyncio


class GameManager:
    # Manage ongoing games of a type, including storage, add and removal
    def __init__(self, bot):
        self.bot = bot
        self.games_in_progress = {}

    def is_valid_user(self, host):
        return host not in self.games_in_progress

    async def check_valid_user(self, host):
        if self.is_valid_user(host):
            return True
        else:
            await self.bot.say("Please finish your current game first.")

    def add_game(self, game):
        self.games_in_progress[game.host] = game

    def get_game(self, ctx):
        author = ctx.message.author
        if author in self.games_in_progress:
            return self.games_in_progress[author]

    def remove_game(self, ctx):
        author = ctx.message.author
        self.games_in_progress.pop(author)

    async def set_time_limit(self, game):
        time_left = game.max_time_left

        while game.in_progress:
            await asyncio.sleep(1.0)
            time_left -= 1
            if time_left == 20:
                await self.low_time_warning(game)
            if time_left == 0:
                await self.time_out(game)
                break
        return True

    async def low_time_warning(self, game):
        host = game.host_name
        await self.bot.say(f"{host} has 20 seconds left!")

    async def time_out(self, game):
        host = game.host_name
        await self.bot.say(f"Time limit elapsed. {host}'s game has ended.")
        await self.end_game(game)

    async def end_game(self, game):
        game.in_progress = False
        self.games_in_progress.pop(game.host)
