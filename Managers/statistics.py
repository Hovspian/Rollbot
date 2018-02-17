import discord

from Core.helper_functions import message_without_command
from Managers.remote_data_manager import RemoteDataManager


class StatisticsBot:
    def __init__(self, bot, data_manager: RemoteDataManager):
        self.gold_stats = GoldStats(bot, data_manager)

    async def query_gold(self, ctx, query):
        if query:
            await self.gold_stats.query_user_gold(ctx, query)
        else:
            await self.gold_stats.say_gold(ctx)

    async def query_winnings(self, ctx):
        await self.gold_stats.say_winnings(ctx)

    async def query_losses(self, ctx, query):
        if query:
            await self.gold_stats.query_user_losses(ctx, query)

    async def butt_counter(self):
        pass


class GoldStats:
    def __init__(self, bot, data_manager):
        self.bot = bot
        self.data_manager = data_manager

    async def say_gold(self, ctx):
        user = ctx.message.author
        gold = self.data_manager.get_gold(user)
        if gold:
            await self.bot.say(f"You have {gold} gold.")
        else:
            await self.bot.say("You don't have any gold. Play a game?")

    async def query_user_gold(self, ctx, query):
        member = ctx.message.server.get_member_named(query)
        if member is None:
            await self.bot.say(f"{query} is not a user on the server.")
            return
        await self._say_user_gold(member)

    async def _say_user_gold(self, query_user):
        gold = self.data_manager.get_gold(query_user)
        if gold:
            await self.bot.say(f"{query_user.display_name} has {gold} gold.")
        else:
            await self.bot.say(f"{query_user.display_name} doesn't have any gold.")

    async def say_winnings(self, ctx):
        user = ctx.message.author
        gold_stats = await self.get_formatted_gold_stats(user, stat_type='won')
        if len(gold_stats) > 0:
            gold_stats.insert(0, "You won from")
            await self.bot.say('\n'.join(gold_stats))
        else:
            await self.bot.say("You don't have any statistics yet.")

    async def query_user_losses(self, ctx, query):
        member = ctx.message.server.get_member_named(query)
        if member is None:
            await self.bot.say(f"{query} is not a user on the server.")
            return
        await self.say_losses(member)

    async def say_losses(self, member):
        losses = await self.get_formatted_gold_stats(member, stat_type='lost')
        if len(losses) > 0:
            losses.insert(0, f"{member.display_name} lost to")
            statistics = '\n'.join(losses)
            await self.bot.say(statistics)
        else:
            await self.bot.say(f"{member.display_name} doesn't have any statistics yet.")

    async def get_formatted_gold_stats(self, user, stat_type):
        gold_stats = self.data_manager.get_gold_stats(user)
        formatted_stats = []

        for other_user_id, gold in gold_stats.items():
            filtered_stat = await self.filter_stat(other_user_id, gold, stat_type)
            if filtered_stat is not None:
                formatted_stats.append(filtered_stat)

        return formatted_stats

    async def filter_stat(self, user_id, gold, stat_type):
        user = await self.bot.get_user_info(user_id)
        amount = gold[stat_type]
        if amount > 0:
            return f"{user.display_name}: {amount} gold"
