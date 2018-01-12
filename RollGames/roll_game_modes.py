import asyncio
from RollGames.rollgame import RollGame
from RollGames.roll import Roll
from discord.ext.commands.context import Context
from Managers.data_manager import SessionDataManager


class StaticRollGame(RollGame):
    def __init__(self, bot, data_manager: SessionDataManager, ctx : Context, bet):
        super().__init__(bot, data_manager, ctx, bet)

    async def wait_for_rolls(self, max):
        while len(self.users) > len(self.player_rolls):
            if max == 100:
                await self.bot.wait_for_message(content='/roll', channel=self.ctx.message.channel)
            else:
                await self.bot.wait_for_message(content=f'/roll {max}', channel=self.ctx.message.channel)
            await asyncio.sleep(0.01)
            if self.last_roll.roller in self.users and self.last_roll.roller not in self.player_rolls:
                self.player_rolls.append((self.last_roll.roller, self.last_roll.rolled))
                await self.bot.say("Roll counted")
            await asyncio.sleep(0.01)

    async def determine(self, rolls: list):
        """Determines the winner or loser of a game. If there is a tie, it will reroll for them."""

        rolls.sort(key=lambda roll: roll[1])

        lowest = rolls[0][1]
        lowest_rollers = []
        low_index = 0
        while low_index < len(rolls) and rolls[low_index][1] == lowest:
            lowest_rollers.append(rolls[low_index][0])
            low_index += 1

        highest = rolls[len(rolls) - 1][1]
        highest_rollers = []
        high_index = len(rolls) - 1
        while high_index >= 0 and rolls[high_index][1] == highest:
            highest_rollers.append(rolls[high_index][0])
            high_index -= 1

        if len(lowest_rollers) > 1:
            loser_reroll = []
            for person in lowest_rollers:
                the_roll = await self.forced_roll(person, 100)
                loser_reroll.append((the_roll.roller, the_roll.rolled))
            result = await self.determine(loser_reroll)
            loser = result[0][0]
        else:
            loser = lowest_rollers[0]

        if len(highest_rollers) > 1:
            winner_reroll = []
            for person in highest_rollers:
                the_roll = await self.forced_roll(person, 100)
                winner_reroll.append((the_roll.roller, the_roll.rolled))
            result = await self.determine(winner_reroll)
            winner = result[1][0][0]
        else:
            winner = highest_rollers[0]

        result = [(loser, lowest), [(winner, highest)]]
        return result


class NormalRollGame(StaticRollGame):
    def __init__(self, bot, data_manager: SessionDataManager, ctx, bet):
        super().__init__(bot, data_manager, ctx, bet)

    def create_message(self, ctx):
        host = ctx.message.author.display_name
        return f"{host} is creating a normal roll with {self.bet}g bet. Type /join in the next 20 seconds to join."

    def play_message(self):
        return "Start rolling from 1-100."

    async def determine(self, rolls : list):
        result = await super().determine(rolls)
        result.append(self.bet)

        loser = result[0][0]
        winner = result[1][0][0]
        self.result[loser] = -result[2]
        self.result[winner] = result[2]

        return result


class DifferenceRollGame(StaticRollGame):
    def __init__(self, bot, data_manager: SessionDataManager, ctx, bet):
        super().__init__(bot, data_manager, ctx, bet)

    def create_message(self, ctx):
        host = ctx.message.author.display_name
        return f"{host} is creating a difference roll with {self.bet}g bet. Type /join in the next 20 seconds to join."

    def play_message(self):
        return f"Start rolling from 1-{self.bet}."

    async def determine(self, rolls: list):
        result = await super().determine(rolls)
        difference = result[1][1][0] - result[0][1]
        result.append(difference)

        loser = result[0][0]
        winner = result[1][0][0]
        self.result[loser] = -result[2]
        self.result[winner] = result[2]

        return result


class CountdownRollGame(RollGame):
    def __init__(self, bot, data_manager: SessionDataManager, ctx, bet):
        super().__init__(bot, data_manager, ctx, bet)

    def create_message(self, ctx):
        host = ctx.message.author.display_name
        return f"{host} is creating a countdown roll with {self.bet}g bet. Type /join in the next 20 seconds to join."

    def play_message(self):
        return "Starting to play a countdown roll game."

    async def wait_for_rolls(self, max):
        self.last_roll = Roll(self.bet, None, self.bet)
        while self.last_roll.rolled > 1:
            for player in self.users:
                await asyncio.sleep(0.01)
                if self.last_roll.rolled == 1:
                    index = self.users.index(player)
                    loser_index = (index - 1) % len(self.users)
                    self.player_rolls[0] = self.users[loser_index]

                    return
                await self.bot.say(f'Waiting for roll to {self.last_roll.rolled} from {self.get_name(player)}')
                if self.last_roll.rolled == 100:
                    await self.bot.wait_for_message(content='/roll', author=player, channel=self.ctx.message.channel)
                else:
                    await self.bot.wait_for_message(content=f'/roll {self.last_roll.rolled}', author=player,
                                                    channel=self.ctx.message.channel)

                await asyncio.sleep(0.5)

    async def determine(self, rolls : list):
        winners = []
        for player in self.users:
            if player is not rolls[0]:
                winners.append(self.get_name(player))
        owed = self.bet // len(winners)

        loser = rolls[0]
        self.result[loser] = -self.bet

        for player in winners:
            self.result[player] = owed

        result = [rolls[0], winners, owed]
        return result
