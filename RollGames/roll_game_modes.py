import asyncio, random
from RollGames.rollgame import RollGame
from RollGames.roll import Roll
from discord.ext.commands.context import Context
from Managers.data_manager import SessionDataManager


class StaticRollGame(RollGame):
    def __init__(self, bot, data_manager: SessionDataManager, ctx : Context, bet):
        super().__init__(bot, data_manager, ctx, bet)
        self.player_rolls = []

    async def wait_for_rolls(self):
        while len(self.users) > len(self.player_rolls):
            await asyncio.sleep(1)

    async def determine(self):
        """Determines the winner or loser of a game. If there is a tie, it will reroll for them."""

        self.player_rolls.sort(key=lambda roll: roll[1])

        lowest = self.player_rolls[0][1]
        lowest_rollers = []
        low_index = 0
        while low_index < len(self.player_rolls) and self.player_rolls[low_index][1] == lowest:
            lowest_rollers.append(self.player_rolls[low_index][0])
            low_index += 1

        highest = self.player_rolls[len(self.player_rolls) - 1][1]
        highest_rollers = []
        high_index = len(self.player_rolls) - 1
        while high_index >= 0 and self.player_rolls[high_index][1] == highest:
            highest_rollers.append(self.player_rolls[high_index][0])
            high_index -= 1

        loser = lowest_rollers[random.randint(0, len(lowest_rollers) - 1)]
        winner = highest_rollers[random.randint(0, len(highest_rollers) - 1)]

        result = [loser, winner]
        return result


class NormalRollGame(StaticRollGame):
    def __init__(self, bot, data_manager: SessionDataManager, ctx, bet):
        super().__init__(bot, data_manager, ctx, bet)

    def play_message(self):
        return "Start rolling from 1-100"

    async def determine(self):
        super_result = await super().determine()
        loser = super_result[0]
        winner = super_result[1]
        if self.player_rolls[0][1] == self.player_rolls[len(self.player_rolls) - 1][1]:
            owed = 0
        else:
            owed = self.bet

        result = [(loser, -owed), [(winner, owed)]]
        return result

    def add_roll(self, roll):
        if roll.roller in self.users and roll.roller not in self.player_rolls and roll.max == 100:
            self.player_rolls.append((roll.roller, roll.rolled))


class DifferenceRollGame(StaticRollGame):
    def __init__(self, bot, data_manager: SessionDataManager, ctx, bet):
        super().__init__(bot, data_manager, ctx, bet)

    def play_message(self):
        if self.bet > 0:
            return f"Start rolling from 1-{self.bet}"
        else:
            return "Start rolling from 1-100"

    async def determine(self):
        super_result = await super().determine()
        loser = super_result[0]
        winner = super_result[1]
        owed = self.player_rolls[len(self.player_rolls) - 1][1] - self.player_rolls[0][1]

        result = [(loser, -owed), [(winner, owed)]]
        return result

    def add_roll(self, roll):
        if roll.roller in self.users and roll.roller not in self.player_rolls and \
                (roll.max == self.bet or (roll.max == 100 and self.bet < 1)):
            self.player_rolls.append((roll.roller, roll.rolled))


class CountdownRollGame(RollGame):
    def __init__(self, bot, data_manager: SessionDataManager, ctx, bet):
        super().__init__(bot, data_manager, ctx, bet)
        if bet > 1:
            self.next_roll = bet
        else:
            self.next_roll = 100

    def play_message(self):
        return f"Waiting for roll to {self.next_roll} from {self.get_name(self.users[0])}"

    async def wait_for_rolls(self):
        while self.next_roll > 1:
            await asyncio.sleep(1)

    async def determine(self):
        result = []
        loser = self.users[-1]
        winners = self.users[:-1]
        owed = self.bet // len(winners)
        result[0] = (loser, -self.bet)

        winner_list = []
        for player in winners:
            winner_list.append((player, owed))
        result[1] = winner_list

        return result

    async def add_roll(self, roll):
        if self.next_roll == 1:
            return
        if roll.roller is self.users[0] and roll.max == self.next_roll:
            self.next_roll = roll.rolled
            self.users.remove(roll.roller)
            self.users.append(roll.roller)
            if roll.rolled > 1:
                await self.bot.say(f"Waiting for roll to {self.next_roll} from {self.users[0].display_name}")
