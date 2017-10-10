

class ChannelManager:

    # Applies the restriction of one ongoing game per channel.

    def __init__(self, bot):
        self.active_games = {}
        self.bot = bot

    async def is_valid_channel_host(self, ctx) -> bool:
        if not self.is_game_host(ctx):
            host = self.get_game_host(ctx)
            if host:
                await self.bot.say(f'The current game host is {host}. Please make a game in another channel.')
            return False
        return True

    def is_game_host(self, ctx) -> bool:
        game_host = self.get_game_host(ctx)
        author_object = ctx.message.author
        return game_host == author_object

    def get_game_host(self, ctx) -> str:
        game = self.get_game(ctx)
        if game:
            return game.host.display_name

    def get_game(self, ctx):
        channel = ctx.message.channel
        if channel in self.active_games:
            return self.active_games[channel]

    async def check_valid_new_game(self, ctx):
        channel = ctx.message.channel
        if self.is_game_in_channel(channel):
            await self.bot.say('Another game is already underway in this channel.')
            return False
        return True

    def add_game_in_session(self, ctx, game):
        channel = ctx.message.channel
        self.active_games[channel] = game

    async def add_user_to_game(self, ctx):
        channel = ctx.message.channel
        user = ctx.message.author
        self.active_games[channel].add_user(user)
        await self.bot.say("{} joined the game.".format(user.display_name))

    def vacate_channel(self, ctx):
        channel = ctx.message.channel
        self.active_games.pop(channel)

    def is_game_in_channel(self, channel) -> bool:
        return channel in self.active_games.keys()

    def is_game_in_progress(self, channel) -> bool:
        if self.is_game_in_channel(channel):
            game = self.active_games[channel]
            return game.in_progress

    def is_user_in_game(self, channel, user) -> bool:
        if self.is_game_in_channel(channel):
            game = self.active_games[channel]
            return user in game.players

    async def check_valid_user(self, ctx) -> bool:
        error = self._check_invalid_user_error(ctx)
        if error:
            await self.bot.say(error)
        else:
            return True

    def _check_invalid_user_error(self, ctx):
        channel = ctx.message.channel
        user = ctx.message.author
        error = None
        if not self.is_game_in_channel(channel):
            error = "No game in this channel."
        elif self.is_game_in_progress(channel):
            error = "Sign ups are closed for this game."
        elif self.is_user_in_game(channel, user):
            error = "{} is already in the game.".format(user.display_name)
        return error
