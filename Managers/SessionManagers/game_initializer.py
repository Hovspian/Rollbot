from abc import abstractmethod

from Core.core_game_class import GameCore


class SessionOptions:

    # Interface for GameInitializer properties

    def __init__(self, bot, channel_manager, data_manager):
        self.bot = bot
        self.channel_manager = channel_manager
        self.data_manager = data_manager


class GameInitializer:

    """
    For games that have persistence.
    Some games have join timers, while others start immediately.
    Some games have time limits, but not all games need them.
    """

    def __init__(self, options: SessionOptions):
        self.bot = options.bot
        self.channel_manager = options.channel_manager
        self.data_manager = options.data_manager

    @abstractmethod
    def _create_session(self, game: GameCore):
        raise NotImplementedError

    def _add_game(self, ctx, game):
        channel = ctx.message.channel
        self.channel_manager.occupy_channel(channel, game)

    def _remove_game(self, ctx):
        channel = ctx.message.channel
        self.channel_manager.vacate_channel(channel)

    async def _can_create_game(self, ctx) -> bool:
        return await self.channel_manager.is_valid_channel(ctx) and \
                await self._is_valid_new_game(ctx)

    async def _is_valid_new_game(self, ctx) -> bool:
        user = ctx.message.author
        for game in self.channel_manager.get_games():
            if self._is_in_game(game, user):
                await ctx.send("Please finish your current game first.")
                return False
        return True

    @staticmethod
    def _is_in_game(game, user) -> bool:
        return any(in_game_user for in_game_user in game.users if in_game_user is user)
