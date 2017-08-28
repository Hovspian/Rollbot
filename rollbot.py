import discord, random, asyncio, math
from discord.ext import commands

from HammerRace.hammerbot import HammerRaceManager

description = '''A bot to roll for users and provide rolling games.'''
bot = commands.Bot(command_prefix='/', description=description)
client = discord.Client()


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('-' * len(bot.user.id))


class Roll:
    def __init__(self,rolled,roller,max):
        self.rolled = rolled
        self.roller = roller
        self.max = max

last_roll = [Roll(0, None, 0)]


@bot.command(pass_context=True)
async def roll(ctx, max=100):
    """Rolls a random integer between 1 and max. 100 is the default max if another is not given."""
    roller = ctx.message.author

    if max < 1:
        await bot.say('1 is the minimum for rolls.')
        return

    roll = random.randint(1, max)
    last_roll[0] = Roll(roll,roller,max)
    await bot.say("{} rolled {} (1-{})".format(roller.display_name, roll, max))
    # return last_roll[0]


@bot.command(pass_context=True)
async def start(ctx, mode: str, bet=100):
    """Starts the game mode specified with the given bet. If no bet is given, 100 is chosen as the default."""
    valid_modes = ['normal', 'difference', 'countdown']
    if mode not in valid_modes:
        await bot.say('Invalid game mode.')
        return
    if bet < 1:
        await bot.say('1 is the minimum for bets.')
        return


    starter = ctx.message.author
    channel = ctx.message.channel

    the_game = Game(mode,bet,channel,starter)
    await the_game.play()


class Game:
    # from rollbot import bot

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
        lowest = math.inf
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
            await bot.say("There is a tie for highest roll. Forcing rerolls to determine winner.")
            highest_dict = {}
            for person in highest_rollers:
                self.forced_roll(person, 100)
            self.determine(highest_dict, True)

        while len(lowest_rollers) > 1 and not winner:
            await bot.say("There is a tie for lowest roll. Forcing rerolls to determine loser.")
            lowest_dict = {}
            for person in lowest_rollers:
                self.forced_roll(person, 100)
            self.determine(lowest_dict, False)

        if winner:
            return highest_rollers[0]
        else:
            return lowest_rollers[0]

    @bot.command(pass_context=True)
    async def join(ctx, self):
        """Allows the user to join the current game"""
        if ctx.message.channel != self.channel:
            return
        player = ctx.message.author
        if player not in self.players:
            self.players.append(player)
            await bot.say('{} joined the game.'.format(self.get_name(player)))
        else:
            await bot.say('{} is already in the game.'.format(self.get_name(player)))

    async def normal(self, bet):
        """Begins a normal game with the specified bet. In normal games, everyone rolls 1-100 and the lowest roller owes
        the highest rolled the total amount betted."""
        await bot.say("Starting normal roll with {}g bet.".format(bet))


        while len(self.players) > len(self.player_rolls):
            await bot.wait_for_message(content='/roll', channel=self.channel)
            await asyncio.sleep(0.01)
            if last_roll[0].roller in self.players and last_roll[0].roller not in self.player_rolls:
                self.player_rolls[last_roll[0].roller] = last_roll[0].rolled

        winner = await self.determine(self.player_rolls, True)
        loser = await self.determine(self.player_rolls, False)

        await bot.say("{} owes {} {}g".format(self.get_name(loser), self.get_name(winner), bet))

    async def difference(self, bet):
        """Begins a difference game with the specified bet. In difference games, everyone rolls 1-bet and the lowest
        roller owes the highest roller the difference between their rolls."""
        await bot.say("Starting difference roll with {}g bet.".format(bet))

        while len(self.players) > len(self.player_rolls):
            if bet == 100:
                await bot.wait_for_message(content='/roll', channel=self.channel)
            else:
                await bot.wait_for_message(content='/roll {}'.format(bet), channel=self.channel)
            await asyncio.sleep(0.01)
            if last_roll[0].roller in self.players and last_roll[0].roller not in self.player_rolls:
                self.player_rolls[last_roll[0].roller] = last_roll[0].rolled

        winner = await self.determine(self.player_rolls, True)
        loser = await self.determine(self.player_rolls, False)
        the_difference = self.player_rolls[winner] - self.player_rolls[loser]
        await bot.say("{} owes {} {}g".format(self.get_name(loser), self.get_name(winner), the_difference))

    async def countdown(self, bet):
        """Starts a countdown game with the specified bet. In countdown games, the starter rolls 1-bet then everyone
        takes turns rolling 1-previous roll until somebody rolls 1 and loses. The winners receive the bet, evenly split
        among everyone."""
        await bot.say("Starting countdown roll with {}g bet.".format(bet))

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
                    for player in self.players:
                        if player is not loser:
                            winners.append(self.get_name(player))
                    owed = bet // len(winners)

                    await bot.say("{} owes {} {}g".format(self.get_name(loser), ', '.join(winners), owed))
                    return
                await bot.say('Waiting for roll to {} from {}'.format(last_roll[0].rolled, self.get_name(player)))
                if last_roll[0].rolled == 100:
                    await bot.wait_for_message(content='/roll',author=player,channel=self.channel)
                else:
                    await bot.wait_for_message(content='/roll {}'.format(last_roll[0].rolled), author=player,
                                               channel=self.channel)

    @staticmethod
    async def forced_roll(player: discord.member.Member, max: int):
        """Automatically rolls for a player"""
        roll = random.randint(1, max)
        last_roll[0] = Roll(roll, player, max)
        return last_roll[0]

    @staticmethod
    def get_name(author):
        return author.display_name

    async def play(self):
        await bot.say("Starting new {} roll. Type /join in the next 15 seconds to join.".format(self.mode))
        await asyncio.sleep(15.0)

        if len(self.players) < 2:
            await bot.say('Not enough players.')
            bot.remove_command('join')
            return

        bot.remove_command('join')

        if self.mode == 'normal':
            await self.normal(self.bet)
        elif self.mode == 'difference':
            await self.difference(self.bet)
        else:
            await self.countdown(self.bet)


bot.remove_command('help')


@bot.command(pass_context=True)
async def hammerbot(ctx):
    hammer = HammerRaceManager()
    hammer.init_race()
    await bot.say(hammer.round_report())

    while hammer.race_in_progress:
        await asyncio.sleep(2.0)
        hammer.next_round()
        await bot.say(hammer.round_report())

    question = str(ctx.message.content)
    remove_command_msg = 11
    if question != '':
        await bot.say('"' + question[remove_command_msg:] + '":')

    await bot.say(hammer.winner_report())


@bot.command()
async def help():
    await bot.say("```Rollbot commands: "
                  "\n   /roll <max> - Rolls a random number between 1 and max. 100 is the default max. "
                  "\n   /start <mode> <bet> - Starts a new game. The bet is set to 100 if not specified. "
                  "\n   Note: only one game can be in progress at a time. "
                  "\n   /join - Join the current game. "
                  "\n\nGame modes: "
                  "\n   normal - everyone rolls 1-100. The lowest roller owes the highest roller the bet. "
                  "\n   difference - everyone rolls 1-bet and the lowest roller owes the highest roller the difference "
                  "between the rolls."
                  "\n   countdown - the starter rolls 1-bet then everyone takes turns rolling 1-previous roll until "
                  "someone rolls 1 and loses. The winnings are split between everyone else. "
                  "\n   Note: if there is a tie then I will do more rolls on my own to decide the winner```")


bot.run('MzUwMzU0OTQzMjQ2NTk4MTQ2.DIC1AA.rsimVu4-dQ5oVrffSu5P_lLmNJY')

