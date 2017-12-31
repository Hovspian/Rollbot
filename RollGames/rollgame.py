import discord, random, asyncio
from RollGames.roll import Roll
from Managers.data_manager import SessionDataManager


class RollGame:
    def __init__(self, bot, data_manager: SessionDataManager, ctx, bet):
        self.bot = bot
        self.data_manager = data_manager
        self.bet = bet
        self.ctx = ctx
        self.users = []
        self.player_rolls = []
        self.result = {}
        self.in_progress = False
        self.last_roll = Roll(0, None, 0)

    @staticmethod
    async def forced_roll(player: discord.member.Member, max: int):
        """Automatically rolls for a player"""
        roll = random.randint(1, max)
        the_roll = Roll(roll, player, max)
        return the_roll

    @staticmethod
    def get_name(author):
        return author.display_name

    async def add(self, player: discord.member.Member):
        self.users.append(player)

    async def wait_for_rolls(self, max):
        raise NotImplementedError

    async def determine(self, rolls):
        raise NotImplementedError

    def create_message(self, ctx):
        raise NotImplementedError

    def play_message(self):
        raise NotImplementedError