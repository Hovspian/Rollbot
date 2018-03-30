import asyncio


class ChannelManager:

    """
    Restricts one ongoing game per channel.
    Methods called by GameInitializer and bot commands.
    """

    def __init__(self, bot):
        self.bot = bot
        self.active_games = {}  # Key: channel ID, value: GameCore
        self.join_timers = {}  # Key: game.host (Discord member), value: JoinTimer

    def get_game(self, channel):
        if self._is_game_in_channel(channel):
            return self.active_games[channel]

    def get_games(self):
        return self.active_games

    def occupy_channel(self, channel, game) -> None:
        self.active_games[channel] = game

    def vacate_channel(self, channel) -> None:
        self.active_games.pop(channel)

    async def add_join_timer(self, host, join_timer):
        self.join_timers[host] = join_timer
        await join_timer.run()
        self.remove_join_timer(host)

    def remove_join_timer(self, host):
        self.join_timers.pop(host)

    async def check_valid_forcestart(self, ctx):
        error = self._get_invalid_forcestart_error(ctx)
        if error:
            await self._say_temp_message(error)
            return
        user = ctx.message.author
        timer = self.join_timers[user]
        timer.cancel_timer()
        await self.bot.add_reaction(ctx.message, '👌')

    def quit(self):
        # User quits the game (if possible)
        pass

    async def is_valid_channel(self, ctx) -> bool:
        channel = ctx.message.channel
        if not self._is_game_in_channel(channel):
            return True
        await self._say_temp_message("Another game is already underway in this channel.")
        return False

    async def check_valid_join(self, ctx) -> None:
        error = self._get_invalid_join_error(ctx)
        if error:
            await self._say_temp_message(error)
        else:
            await self._add_user_to_game(ctx)

    async def check_valid_add_ai(self, ctx) -> None:
        error = self._get_invalid_add_ai_error(ctx)
        if error:
            await self._say_temp_message(error)
        else:
            await self.add_ai_to_game(ctx)

    async def _add_user_to_game(self, ctx) -> None:
        channel = ctx.message.channel
        user = ctx.message.author
        game = self.get_game(channel)
        game.add_user(user)
        await self.bot.say(f"{user.display_name} joined the game.")
        await self._check_player_capacity(game)

    async def add_ai_to_game(self, ctx) -> None:
        channel = ctx.message.channel
        game = self.get_game(channel)
        try:
            await game.add_ai()
            await self._check_player_capacity(game)
        except AttributeError:
            await self._say_temp_message("This game currently doesn't support AI players.")

    async def _check_player_capacity(self, game) -> None:
        """
        The game auto starts when the max number of players has been reached.
        """
        if game.is_max_num_players():
            timer = self.join_timers[game.host]
            timer.cancel_timer()
            await self._say_temp_message("The game room is now full.")

    def _get_invalid_forcestart_error(self, ctx) -> str or None:
        channel = ctx.message.channel
        user = ctx.message.author
        error = None
        if not self._is_game_in_channel(channel):
            error = "No game in this channel."
        elif self._is_game_in_progress(channel):
            error = "Game is already in progress."
        elif not self._is_user_host(channel, user):
            error = "Only the game host can forcestart the game."
        return error

    def _get_invalid_join_error(self, ctx) -> str or None:
        channel = ctx.message.channel
        user = ctx.message.author
        error = None
        if not self._is_game_in_channel(channel):
            error = "No game in this channel."
        elif self._is_game_in_progress(channel):
            error = "Sign ups are closed for this game."
        elif self._is_user_in_game(channel, user):
            error = f"{user.display_name} is already in the game."
        return error

    def _get_invalid_add_ai_error(self, ctx) -> str or None:
        channel = ctx.message.channel
        user = ctx.message.user
        error = None
        if not self._is_game_in_channel(channel):
            error = "No game in this channel."
        elif self._is_game_in_progress(channel):
            error = "Adding players is closed for this game."
        elif not self._is_user_in_game(channel, user):
            error = "Please join the game before trying to add AI players."
        return error

    def _is_game_in_channel(self, channel) -> bool:
        return channel in self.active_games.keys()

    def _is_game_in_progress(self, channel) -> bool:
        game = self.active_games[channel]
        return game.in_progress

    def _is_user_in_game(self, channel, user) -> bool:
        # Search the game's users for a match
        game = self.active_games[channel]
        return any(in_game_user for in_game_user in game.users if in_game_user is user)

    def _is_user_host(self, channel, user) -> bool:
        game = self.active_games[channel]
        return user == game.host

    async def _say_temp_message(self, message: str):
        temp = await self.bot.say(message)
        await asyncio.sleep(5.0)
        await self.bot.delete_message(temp)