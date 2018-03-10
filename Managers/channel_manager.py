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
            temp_message = await self.bot.say(error)
        else:
            user = ctx.message.author
            timer = self.join_timers[user]
            timer.cancel_timer()
            temp_message = await self.bot.say(':ok_hand:')
        await self._auto_delete_message(temp_message)

    def quit(self):
        # User quits the game (if possible)
        pass

    async def is_valid_channel(self, ctx) -> bool:
        channel = ctx.message.channel
        if self._is_game_in_channel(channel):
            temp_message = await self.bot.say("Another game is already underway in this channel.")
            await self._auto_delete_message(temp_message)
        else:
            return True

    async def check_valid_join(self, ctx):
        error = self._get_invalid_join_error(ctx)
        if error:
            temp_message = await self.bot.say(error)
            await self._auto_delete_message(temp_message)
        else:
            await self._add_user_to_game(ctx)

    async def _add_user_to_game(self, ctx) -> None:
        channel = ctx.message.channel
        user = ctx.message.author
        game = self.active_games[channel]
        game.add_user(user)
        await self.bot.say(f"{user.display_name} joined the game.")
        await self._check_player_capacity(game)

    async def _check_player_capacity(self, game):
        """
        The game auto starts when the max number of players has been reached.
        """
        if game.is_max_num_players():
            timer = self.join_timers[game.host]
            timer.cancel_timer()
            await self.bot.say("The game room is now full.")

    def _get_invalid_forcestart_error(self, ctx) -> str:
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

    def _get_invalid_join_error(self, ctx) -> str:
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

    async def _auto_delete_message(self, message):
        await asyncio.sleep(5.0)
        await self.bot.delete_message(message)