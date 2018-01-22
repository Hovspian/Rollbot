import discord, random, asyncio

from Core.core_game_class import GameCore
from RollGames.roll import Roll
from Managers.data_manager import SessionDataManager


class RollGame(GameCore):
    def __init__(self, bot, ctx, bet):
        super().__init__(ctx)
        self.bot = bot
        self.bet = bet
        self.player_rolls = []
        self.in_progress = False
        self.result = []
        self.invalid_players_error = "A roll game needs at least two players."

    async def start_rolls(self):
        if self.valid_num_players():
            await self.start_game()
            self.end_game()
        else:
            await self.bot.say(self.invalid_players_error)

    async def start_game(self):
        super().start_game()
        await self.bot.say("Waiting for rolls")
        await self.wait_for_rolls(self.bet)
        await self.bot.say("Determining results")
        result = await self.determine(self.player_rolls)
        loser = self.get_name(result[0][0])
        winner = self.get_name(result[1][0])
        the_difference = result[1][1] - result[0][1]
        if the_difference == 0:
            await self.bot.say("It's a tie.")
        else:
            await self.bot.say(f"{loser} owes {winner} {result[2]}g")

    def valid_num_players(self) -> bool:
        return len(self.players) > 1

    def add_user(self, user):
        super().add_user(user)
        self.add_player(user)

    @staticmethod
    async def forced_roll(player: discord.member.Member, max: int):
        """Automatically rolls for a player"""
        roll = random.randint(1, max)
        the_roll = Roll(roll, player, max)
        return the_roll

    @staticmethod
    def get_name(author):
        return author.display_name

    async def wait_for_rolls(self, max):
        raise NotImplementedError

    async def determine(self, rolls):
        raise NotImplementedError
