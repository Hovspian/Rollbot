import discord, random, asyncio
from RollGames.roll import Roll


last_roll = [Roll(0, None, 0)]


class RollGame:
    def __init__(self, bot, game_mode, bet, channel):
        self.bot = bot
        self.mode = game_mode
        self.bet = bet
        self.channel = channel
        self.players = []
        self.player_rolls = []
        self.in_progress = False

    async def normal(self, bet):
        """Begins a normal game with the specified bet. In normal games, everyone rolls 1-100 and the lowest roller owes
        the highest rolled the total amount betted."""
        await self.bot.say("Starting normal roll with {}g bet.".format(bet))

        await self.wait_for_rolls(100)

        loser_and_winner = await self.determine(self.player_rolls)
        loser = self.get_name(loser_and_winner[0][0])
        winner = self.get_name(loser_and_winner[1][0])
        the_difference = loser_and_winner[1][1] - loser_and_winner[0][1]
        if the_difference:
            await self.bot.say("It's a tie.")
        else:
            await self.bot.say("{} owes {} {}g".format(loser, winner, bet))

    async def difference(self, bet):
        """Begins a difference game with the specified bet. In difference games, everyone rolls 1-bet and the lowest
        roller owes the highest roller the difference between their rolls."""
        await self.bot.say("Starting difference roll with {}g bet.".format(bet))

        await self.wait_for_rolls(bet)

        loser_and_winner = await self.determine(self.player_rolls)
        loser = self.get_name(loser_and_winner[0][0])
        winner = self.get_name(loser_and_winner[1][0])
        the_difference = loser_and_winner[1][1] - loser_and_winner[0][1]
        if the_difference == 0:
            await self.bot.say("It's a tie.")
        else:
            await self.bot.say("{} owes {} {}g".format(loser, winner, the_difference))

    async def wait_for_rolls(self, max):
        while len(self.players) > len(self.player_rolls):
            if max == 100:
                await self.bot.wait_for_message(content='/roll', channel=self.channel)
            else:
                await self.bot.wait_for_message(content='/roll {}'.format(max), channel=self.channel)
            await asyncio.sleep(0.01)
            if last_roll[0].roller in self.players and last_roll[0].roller not in self.player_rolls:
                self.player_rolls.append((last_roll[0].roller, last_roll[0].rolled))

    async def countdown(self, bet):
        """Starts a countdown game with the specified bet. In countdown games, the starter rolls 1-bet then everyone
        takes turns rolling 1-previous roll until somebody rolls 1 and loses. The winners receive the bet, evenly split
        among everyone."""
        await self.bot.say("Starting countdown roll with {}g bet.".format(bet))

        last_roll[0] = Roll(bet, None, bet)
        while last_roll[0].rolled > 1:
            for player in self.players:
                await asyncio.sleep(0.01)
                if last_roll[0].rolled == 1:
                    player_index = self.players.index(player)
                    if player_index == 0:
                        loser_index = len(self.players) - 1
                    else:
                        loser_index = player_index - 1
                    loser = self.players[loser_index]
                    winners = []
                    for winner in self.players:
                        if winner is not loser:
                            winners.append(self.get_name(winner))
                    owed = bet / len(winners)

                    await self.bot.say("{} owes {} {}g".format(self.get_name(loser), ', '.join(winners), owed))
                    return
                await self.bot.say('Waiting for roll to {} from {}'.format(last_roll[0].rolled, self.get_name(player)))
                if last_roll[0].rolled == 100:
                    await self.bot.wait_for_message(content='/roll', author=player, channel=self.channel)
                else:
                    await self.bot.wait_for_message(content='/roll {}'.format(last_roll[0].rolled), author=player,
                                                    channel=self.channel)

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
            winner = result[1][0]
        else:
            winner = highest_rollers[0]

        result = [(loser, lowest), (winner, highest)]
        return result

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
        self.players.append(player)

    async def play(self):
        await self.bot.say("Starting new {} roll. Type /join in the next 15 seconds to join.".format(self.mode))
        await asyncio.sleep(15.0)

        if len(self.players) < 2:
            await self.bot.say('Not enough players.')
            return

        self.in_progress = True
        if self.mode == 'normal':
            await self.normal(self.bet)
        elif self.mode == 'difference':
            await self.difference(self.bet)
        else:
            await self.countdown(self.bet)
        self.in_progress = False



