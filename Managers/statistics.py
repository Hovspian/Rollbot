from Managers.data_manager import SessionDataManager
import discord
from helper_functions import message_without_command


class StatisticsBot:
    def __init__(self, bot, data_manager: SessionDataManager):
        self.bot = bot
        self.data_manager = data_manager

    async def query_gold(self, ctx):
        query = message_without_command(ctx.message.content)
        if query:
            await self._query_user_gold(ctx, query)
        else:
            await self._say_personal_gold(ctx)

    async def _say_personal_gold(self, ctx):
        user = ctx.message.author
        gold = self.data_manager.get_gold(user)
        if gold:
            await self.bot.say(f"You have {gold} gold.")
        else:
            await self.bot.say("You don't have any gold. Play a game?")

    async def _query_user_gold(self, ctx, query):
        message = ctx.message
        query_user = discord.utils.get(message.server.members, name=query)
        if query_user:
            await self._say_user_gold(query_user)
        else:
            await self.bot.say(f"{query} is not a user on the server.")

    async def _say_user_gold(self, query_user):
        gold = self.data_manager.get_gold(query_user)
        if gold:
            await self.bot.say(f"{query_user} has {gold} gold.")
        else:
            await self.bot.say(f"{query_user} does not have any gold.")

