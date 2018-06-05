from operator import itemgetter
from typing import List

import discord

from Core.constants import LINEBREAK, CODE_TAG
from Core.helper_functions import message_without_command
from Managers.remote_data_manager import RemoteDataManager


class StatisticsBot:
    def __init__(self, bot, data_manager: RemoteDataManager):
        self.gold_stats = GoldStats(bot, data_manager)
        self.data_manager = data_manager
        self.bot = bot

    async def query_gold(self, ctx, query) -> None:
        if query:
            message = self.gold_stats.get_user_gold_report(ctx, query)
        else:
            message = self.gold_stats.get_personal_gold_report(ctx)
        await self.bot.say(message)

    async def query_gold_stats(self, ctx, query) -> None:
        if query:
            stats_list = self.gold_stats.query_user_totals(ctx, query)
        else:
            user = ctx.message.author
            stats_list = self.gold_stats.get_totals(user)

        message = self.wrap_statistics(stats_list)
        await self.bot.say(message)

    async def query_winnings(self, ctx, query) -> None:
        if query:
            stats_list = self.gold_stats.query_user_winnings(ctx, query)
        else:
            user = ctx.message.author
            stats_list = self.gold_stats.get_winnings(user)

        message = self.wrap_statistics(stats_list)
        await self.bot.say(message)

    async def query_losses(self, ctx, query) -> None:
        if query:
            stats_list = self.gold_stats.query_user_losses(ctx, query)
        else:
            user = ctx.message.author
            stats_list = self.gold_stats.get_losses(user)

        message = self.wrap_statistics(stats_list)
        await self.bot.say(message)

    @staticmethod
    def wrap_statistics(stats_list: str) -> str:
        return LINEBREAK.join([CODE_TAG,
                               stats_list,
                               CODE_TAG])

    async def stats(self, ctx) -> None:
        pass

    def update_melons(self, ctx, amount: int) -> None:
        self.data_manager.update_melons(ctx, amount)

    def update_butts(self, ctx, amount: int) -> None:
        self.data_manager.update_butts(ctx, amount)

    def update_eggplants(self, ctx, amount: int) -> None:
        self.data_manager.update_eggplants(ctx, amount)

    def update_fuqs(self, ctx, amount: int) -> None:
        self.data_manager.update_fuqs(ctx, amount)

    async def total_butts(self, ctx) -> None:
        butts_dict = self.data_manager.get_server_butts(ctx)
        num_butts = butts_dict['butts']
        num_commands = butts_dict['butts_commands']
        await self.bot.say(f':peach: Total butts on this server: {num_butts} ({num_commands} `/butts`) :peach: ')

    async def global_butts(self) -> None:
        num_butts = 0
        num_commands = 0
        for server in self.bot.servers:
            butts_dict = self.data_manager.get_butts_from_server_id(server.id)
            num_butts += butts_dict['butts']
            num_commands += butts_dict['butts_commands']
        await self.bot.say(f':peach: Global butts: {num_butts} ({num_commands}  `/butts`) :peach:')


class GoldStats:
    def __init__(self, bot, data_manager):
        self.data_manager = data_manager
        self.bot = bot

    def get_personal_gold_report(self, ctx) -> str:
        user = ctx.message.author
        gold = self.data_manager.get_gold(user)
        if gold:
            return f"You have {gold} gold."
        return "You don't have any gold. Play a game?"

    def get_user_gold_report(self, ctx, query) -> str:
        user = ctx.message.server.get_member_named(query)
        if user is None:
            return f"{query} is not a user on the server."
        return self.__get_user_gold(user)

    def query_user_totals(self, ctx, query) -> str:
        user = ctx.message.server.get_member_named(query)
        if user is None:
            return f"{query} is not a user on the server."
        return self.get_totals(user)

    def get_totals(self, user) -> str or None:
        gold_stats = self.__get_formatted_totals(user)
        if len(gold_stats) > 0:
            gold_stats.insert(0, f"{user.display_name}'s stats")
            return LINEBREAK.join(gold_stats)

    def query_user_winnings(self, ctx, query) -> str:
        user = ctx.message.server.get_member_named(query)
        if user is None:
            return f"{query} is not a user on the server."
        return self.get_winnings(user)

    def get_winnings(self, user) -> str or None:
        gold_stats = self.__get_formatted_winnings(user)
        if len(gold_stats) > 0:
            gold_stats.insert(0, f"{user.display_name} won from")
            return LINEBREAK.join(gold_stats)

    def query_user_losses(self, ctx, query) -> str:
        member = ctx.message.server.get_member_named(query)
        if member is None:
            return f"{query} is not a user on the server."
        return self.get_losses(member)

    def get_losses(self, user) -> str or None:
        losses = self.__get_formatted_losses(user)
        if len(losses) > 0:
            losses.insert(0, f"{user.display_name} lost to")
            return LINEBREAK.join(losses)

    def __get_formatted_totals(self, user) -> List[str]:
        return self.__get_formatted_gold_stats('total', user)

    def __get_formatted_winnings(self, user) -> List[str]:
        return self.__get_formatted_gold_stats('won', user)

    def __get_formatted_losses(self, user) -> List[str]:
        return self.__get_formatted_gold_stats('lost', user)

    def __get_formatted_gold_stats(self, stat_type: str, user) -> List[str]:
        stats = self.__get_sorted_stats(stat_type, user)
        return [self.__get_details(i, stat) for i, stat in enumerate(stats)]

    def __get_sorted_stats(self, stat_type: str, user) -> List[dict]:
        """
        Arrange gold stats by most to least.
        """
        gold_stats = self.data_manager.get_gold_stats(user)  # dict of dict
        list_stats = []
        for other_user_id, stats in gold_stats.items():
            gold = stats[stat_type]
            if gold == 0:  # Ignore 0 value entries
                continue
            other_user = self.get_known_user(other_user_id)
            if other_user:
                list_stats.append({'user': other_user.display_name,
                                   'gold': gold})

        return sorted(list_stats, key=itemgetter('gold'), reverse=True)

    def get_known_user(self, id_to_match):
        for member in self.bot.get_all_members():
            if member.id == id_to_match:
                return member

    def __get_user_gold(self, query_user) -> str:
        gold = self.data_manager.get_gold(query_user)
        if gold:
            return f"{query_user.display_name} has {gold} gold."
        return f"{query_user.display_name} doesn't have any gold."

    @staticmethod
    def __get_details(position: int, stat: dict) -> str:
        user = stat['user']
        gold = stat['gold']
        position += 1  # Start from 1
        return f'{position}) {user}: {gold} gold'
