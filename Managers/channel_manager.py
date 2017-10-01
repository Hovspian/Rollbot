import asyncio

class ChannelManager:

    def __init__(self, bot):
        self.games_in_progress = {}
        self.bot = bot

    def is_game_host(self, ctx):
        game = self.get_game(ctx)
        if game:
            author_object = ctx.message.author
            return game.host == author_object

    def get_game_host(self, ctx):
        game = self.get_game(ctx)
        if game:
            return game.host.display_name

    def get_game(self, ctx):
        channel = ctx.message.channel
        if channel in self.games_in_progress:
            return self.games_in_progress[channel]

    async def check_valid_new_game(self, ctx):
        channel = ctx.message.channel
        if self.is_game_in_channel(channel):
            await self.bot.say('Another game is already underway in this channel.')
        return True

    def add_game_in_progress(self, ctx, game):
        channel = ctx.message.channel
        self.games_in_progress[channel] = game

    async def add_user_to_game(self, channel, user):
        await self.games_in_progress[channel].add(user)

    def vacate_channel(self, channel):
        self.games_in_progress.pop(channel)

    def is_game_in_channel(self, channel):
        return channel in self.games_in_progress.keys()

    def is_game_in_progress(self, channel):
        if self.is_game_in_channel(channel):
            game = self.games_in_progress[channel]
            return game.in_progress

    def is_user_in_game(self, channel, user):
        if self.is_game_in_channel(channel):
            game = self.games_in_progress[channel]
            return user in game.players

    def is_invalid_user_error(self, channel, user):
        error = False
        if not self.is_game_in_channel(channel):
            error = "No game in this channel."
        elif self.is_game_in_progress(channel):
            error = "It's too late to join."
        elif self.is_user_in_game(channel, user):
            error = "{} is already in the game.".format(user.display_name)
        return error
