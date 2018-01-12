from Blackjack.move_checker import BlackjackMoveChecker
from Core.time_limit import TimeLimit
from Blackjack.blackjack_executor import BlackjackExecutor
from Managers.session_options import SessionOptions
from Blackjack.join_timer import BlackjackJoinTimer


class BlackjackInitializer:

    """
    Handles blackjack creation
    """

    def __init__(self, session: SessionOptions):
        self.ctx = session.ctx
        self.bot = session.bot
        self.channel_manager = session.channel_manager
        self.games = {}
        self.join_timers = []

    async def create_game(self, ctx):
        if self.can_create_game(ctx):
            blackjack = BlackjackExecutor(self.bot, self.ctx)
            await self.run_session(blackjack)

    async def run_session(self, blackjack):
        self.add_game(blackjack)
        await self.run_join_timer(blackjack)
        await self.run_time_limit(blackjack)
        self.remove_game(blackjack)

    async def run_join_timer(self, blackjack):
        join_timer = BlackjackJoinTimer(self.bot, blackjack)
        self.join_timers.append(blackjack.host)
        await join_timer.set_join_waiting_period()
        self.join_timers.remove(blackjack.host)

    async def run_time_limit(self, blackjack):
        time_limit = TimeLimit(self.bot, blackjack)
        await time_limit.set_time_limit()

    def add_game(self, blackjack):
        channel = self.ctx.message.channel
        self.channel_manager.add_game(channel, blackjack)
        self.games[blackjack.host] = blackjack

    def remove_game(self, blackjack):
        channel = self.ctx.message.channel
        self.channel_manager.vacate_channel(channel)
        self.games.pop(blackjack.host)

    async def can_create_game(self, ctx) -> bool:
        return self.channel_manager.check_valid_new_game(ctx) and\
                self.check_valid_new_game(ctx)

    async def check_valid_new_game(self, ctx) -> bool:
        user = ctx.message.author
        is_user_in_game = False
        for game in self.games:
            is_user_in_game = self._is_in_game(game, user)
        return is_user_in_game

    @staticmethod
    def _is_in_game(game, user) -> bool:
        return any(in_game_user for in_game_user in game.users if in_game_user is user)


class BlackjackBot:
    def __init__(self, games, bot):
        self.games = games
        self.bot = bot

    def make_move(self, ctx, action):
        move_checker = BlackjackMoveChecker(self.bot)



