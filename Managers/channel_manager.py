class ChannelManager:

    """ Restricts one ongoing game per channel """

    def __init__(self, bot):
        self.active_games = {}
        self.bot = bot

    async def check_valid_new_game(self, ctx) -> bool:
        channel = ctx.message.channel
        if not self._is_game_in_channel(channel):
            return True
        else:
            await self.bot.say("Another game is already underway in this channel.")

    async def check_valid_join(self, ctx) -> bool:
        error = self._check_invalid_join_error(ctx)
        if error:
            await self.bot.say(error)
        else:
            return True

    def add_channel_game(self, channel, game) -> None:
        self.active_games[channel] = game

    def vacate_channel(self, channel) -> None:
        self.active_games.pop(channel)

    async def add_user_to_game(self, ctx) -> None:
        channel = ctx.message.channel
        user = ctx.message.author
        await self.active_games[channel].add_user(user)
        await self.bot.say(f"{user.display_name} joined the game.")

    def _check_invalid_join_error(self, ctx) -> bool:
        channel = ctx.message.channel
        user = ctx.message.author
        error = False
        if not self._is_game_in_channel(channel):
            error = "No game in this channel."
        elif self._is_game_in_progress(channel):
            error = "Sign ups are closed for this game."
        elif self._is_user_in_game(channel, user):
            error = "{} is already in the game.".format(user.display_name)
        return error

    def _is_game_in_channel(self, channel) -> bool:
        return channel in self.active_games.keys()

    def _is_game_in_progress(self, channel) -> bool:
        if self._is_game_in_channel(channel):
            game = self.active_games[channel]
            return game.in_progress

    def _is_user_in_game(self, channel, user) -> bool:
        # Search the game's users attribute
        if self._is_game_in_channel(channel):
            game = self.active_games[channel]
            return any(in_game_user for in_game_user in game.users if in_game_user is user)