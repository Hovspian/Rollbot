import asyncio

class ChannelManager:

    """
    Restricts one ongoing game per channel.
    States controlled by GameInitializer and bot commands.
    """

    def __init__(self, bot):
        self.bot = bot
        self.active_games = {}  # Key: channel ID, value: GameCore
        self.join_timers = {}  # Key: game.host (Discord member), value: JoinTimer

    def get_game(self, channel):
        return self.active_games[channel]

    def get_games(self):
        return self.active_games

    def occupy_channel(self, channel, game) -> None:
        self.active_games[channel] = game

    def vacate_channel(self, channel) -> None:
        self.active_games.pop(channel)

    def add_join_timer(self, host, join_timer):
        self.join_timers[host] = join_timer

    def remove_join_timer(self, host):
        self.join_timers.pop(host)

    def force_start(self):
        # if game in channel and initiator is host
        pass

    def quit(self):
        # User quits the game (if possible)
        pass

    async def is_valid_channel(self, ctx) -> bool:
        channel = ctx.message.channel
        if self._is_game_in_channel(channel):
            temp_message = await self.bot.say("Another game is already underway in this channel.")
            await self._auto_remove_message(temp_message)
        else:
            return True

    async def check_valid_join(self, ctx):
        error = self._get_invalid_join_error(ctx)
        if error:
            temp_message = await self.bot.say(error)
            await self._auto_remove_message(temp_message)
        else:
            self._add_user_to_game(ctx)

    async def _add_user_to_game(self, ctx) -> None:
        channel = ctx.message.channel
        user = ctx.message.author
        await self.active_games[channel].add_user(user)
        await self.bot.say(f"{user.display_name} joined the game.")

    def _get_invalid_join_error(self, ctx) -> bool:
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
        game = self.active_games[channel]
        return game.in_progress

    def _is_user_in_game(self, channel, user) -> bool:
        # Search the game's users for a match
        game = self.active_games[channel]
        return any(in_game_user for in_game_user in game.users if in_game_user is user)

    async def _auto_remove_message(self, message):
        await asyncio.sleep(5.0)
        self.bot.remove_message(message)