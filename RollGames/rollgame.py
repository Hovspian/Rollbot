from abc import abstractmethod

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
        await self.wait_for_rolls()
        await self.determine()

        if self.result[0][1] == 0:
            await self.bot.say("It's a tie")
        else:
            loser = self.get_name(self.result[0][0])
            winners = []
            for tup in self.result[1]:
                winners.append(self.get_name(tup[0]))
            split_winners = ', '.join(winners)
            await self.bot.say(f"{loser} owes {split_winners} {self.result[1][0][1]}g")

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

    @abstractmethod
    async def wait_for_rolls(self):
        raise NotImplementedError

    @abstractmethod
    async def determine(self):
        raise NotImplementedError

    @abstractmethod
    async def add_roll(self, roll):
        raise NotImplementedError
