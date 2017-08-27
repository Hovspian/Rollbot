import discord, random, asyncio
# from discord.ext import commands
from Rollbot import rollbot


class Game:
    def __init__(self, game_mode, bet, channel, starter):
        self.mode = game_mode
        self.bet = bet
        self.channel = channel
        self.starter = starter
        self.players = [starter]
        self.player_rolls = {}

    async def determine(self, rolls: dict, winner: bool):
        """Determines the winner or loser of a game. If there is a tie, it will reroll for them."""
        highest = -1
        lowest = 1000000000
        highest_rollers = []
        lowest_rollers = []
        for player in rolls.keys():
            if rolls[player] > highest:
                highest = rolls[player]
                del highest_rollers[:]
                highest_rollers.append(player)
            elif rolls[player] == highest:
                highest_rollers.append(player)

            if rolls[player] < lowest:
                lowest = rolls[player]
                del lowest_rollers[:]
                lowest_rollers.append(player)
            elif rolls[player] == lowest:
                lowest_rollers.append(player)

        while len(highest_rollers) > 1 and winner:
            await rollbot.bot.say("There is a tie for highest roll. Forcing rerolls to determine winner.")
            highest_dict = {}
            for person in highest_rollers:
                self.forced_roll(person, 100)
            self.determine(highest_dict, True)

        while len(lowest_rollers) > 1 and not winner:
            await rollbot.bot.say("There is a tie for lowest roll. Forcing rerolls to determine loser.")
            lowest_dict = {}
            for person in lowest_rollers:
                self.forced_roll(person, 100)
            self.determine(lowest_dict, False)

        if winner:
            return highest_rollers[0]
        else:
            return lowest_rollers[0]

    @rollbot.bot.command(pass_context=True)
    async def join(self, ctx):
        """Allows the user to join the current game"""
        if ctx.message.channel != self.channel:
            return
        player = get_author(ctx)
        if player not in self.players:
            self.players.append(player)
            await rollbot.bot.say('{} joined the game.'.format(get_name(player)))
        else:
            await rollbot.bot.say('{} is already in the game.'.format(get_name(player)))

    async def normal(self, bet):
        """Begins a normal game with the specified bet. In normal games, everyone rolls 1-100 and the lowest roller owes
        the highest rolled the total amount betted."""
        await rollbot.bot.say("Starting normal roll with {}g bet.".format(bet))

        while len(self.players) > len(self.player_rolls):
            await rollbot.bot.wait_for_message(content='/roll', channel=self.channel)
            await asyncio.sleep(0.01)
            if rollbot.last_roll[0].roller in self.players and rollbot.last_roll[0].roller not in self.player_rolls:
                self.player_rolls[rollbot.last_roll[0].roller] = rollbot.last_roll[0].rolled

        winner = await self.determine(self.player_rolls, True)
        loser = await self.determine(self.player_rolls, False)

        await rollbot.bot.say("{} owes {} {}g".format(get_name(loser), get_name(winner), bet))

    async def difference(self, bet):
        """Begins a difference game with the specified bet. In difference games, everyone rolls 1-bet and the lowest
        roller owes the highest roller the difference between their rolls."""
        await rollbot.bot.say("Starting difference roll with {}g bet.".format(bet))

        while len(self.players) > len(self.player_rolls):
            if bet == 100:
                await rollbot.bot.wait_for_message(content='/roll', channel=self.channel)
            else:
                await rollbot.bot.wait_for_message(content='/roll {}'.format(bet), channel=self.channel)
            await asyncio.sleep(0.01)
            print(self.players)
            print(self.player_rolls)
            if rollbot.last_roll[0].roller in self.players and rollbot.last_roll[0].roller not in self.player_rolls:
                self.player_rolls[rollbot.last_roll[0].roller] = rollbot.last_roll[0].rolled

        winner = await self.determine(self.player_rolls, True)
        loser = await self.determine(self.player_rolls, False)
        the_difference = self.player_rolls[winner] - self.player_rolls[loser]
        await rollbot.bot.say("{} owes {} {}g".format(get_name(loser), get_name(winner), the_difference))

    async def countdown(self, bet):
        """Starts a countdown game with the specified bet. In countdown games, the starter rolls 1-bet then everyone
        takes turns rolling 1-previous roll until somebody rolls 1 and loses. The winners receive the bet, evenly split
        among everyone."""
        await rollbot.bot.say("Starting countdown roll with {}g bet.".format(bet))

        rollbot.last_roll[0] = Roll(bet, None, bet)
        while rollbot.last_roll[0].rolled > 1:
            for player in self.players:
                await asyncio.sleep(0.01)
                if rollbot.last_roll[0].rolled == 1:
                    player_index = self.players.index(player)
                    if player_index == 0:
                        loser_index = len(self.players) - 1
                    else:
                        loser_index = player_index - 1
                    loser = self.players[loser_index]
                    winners = []
                    for player in self.players:
                        if player is not loser:
                            winners.append(get_name(player))
                    owed = bet // len(winners)

                    await rollbot.bot.say("{} owes {} {}g".format(get_name(loser), ', '.join(winners), owed))
                    return
                await rollbot.bot.say('Waiting for roll to {} from {}'.format(last_roll[0].rolled, get_name(player)))
                if rollbot.last_roll[0].rolled == 100:
                    await rollbot.bot.wait_for_message(content='/roll', author=player, channel=self.channel)
                else:
                    await rollbot.bot.wait_for_message(content='/roll {}'.format(last_roll[0].rolled), author=player,
                                               channel=self.channel)

    async def forced_roll(self, player: discord.member.Member, max: int):
        """Automatically rolls for a player"""
        roll = random.randint(1, max)
        rollbot.last_roll[0] = Roll(roll, player, max)
        return rollbot.last_roll[0]

    async def play(self):
        await rollbot.bot.say("Starting new {} roll. Type /join in the next 15 seconds to join.".format(self.mode))
        await asyncio.sleep(5.0)

        # if len(self.players) < 2:
        #     await bot.say('Not enough players.')
        #     await bot.remove_command('join')
        #     return

        rollbot.bot.remove_command('join')

        if self.mode == 'normal':
            await self.normal(self.bet)
        elif self.mode == 'difference':
            await self.difference(self.bet)
        else:
            await self.countdown(self.bet)