import asyncio
import discord
import random
from discord.ext import commands

from HammerRace.hammerbot import HammerRaceManager

description = '''A bot to roll for users and provide rolling games.'''
bot = commands.Bot(command_prefix='/', description=description)
client = discord.Client()

class Roll:
    rolled = 0   # int that holds the rolled number
    roller = None   # str that holds the person who rolled
    max = 0      # int that holds the max of the roll

    def __init__(self,rolled,roller,max):
        self.rolled = rolled
        self.roller = roller
        self.max = max


last_roll = [Roll(0,None,0)]

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('-' * len(bot.user.id))


async def forced_roll(player : discord.member.Member, max : int):
    """Automatically rolls for a player"""
    roll = random.randint(1,max)
    last_roll[0] = Roll(roll,player,max)
    return last_roll[0]


async def determine(rolls : dict, winner : bool):
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
        elif rolls[player] < lowest:
            lowest_rollers.append(player)

    while len(highest_rollers) > 1 and winner:
        await bot.say("There is a tie for highest roll. Forcing rerolls to determine winner.")
        highest_dict = {}
        for person in highest_rollers:
            forced_roll(person, 100)
        determine(highest_dict,True)

    while len(lowest_rollers) > 1 and not winner:
        await bot.say("There is a tie for lowest roll. Forcing rerolls to determine loser.")
        lowest_dict = {}
        for person in lowest_rollers:
            forced_roll(person, 100)
        determine(lowest_dict,False)

    if winner:
        return highest_rollers[0]
    else:
        return lowest_rollers[0]


def get_author(ctx):
    return ctx.message.author


def get_name(author):
    return author.display_name


@bot.command(pass_context=True)
async def roll(ctx, max=100):
    """Rolls a random integer between 1 and max. 100 is the default max if another is not given."""

    name = get_author(ctx)

    if max < 1:
        await bot.say('1 is the minimum for rolls.')
        return

    roll = random.randint(1, max)
    last_roll[0] = Roll(roll,name,max)
    await bot.say("{} rolled {} (1-{})".format(get_name(name), roll, max))
    return last_roll[0]


@bot.command(pass_context=True)
async def start(ctx, mode: str, bet=100):
    """Starts the game mode specified with the given bet. If no bet is given, 100 is chosen as the default."""
    valid_modes = ['normal', 'difference', 'countdown']
    if mode not in valid_modes:
        await bot.say('Invalid game mode.')
        return

    starter = get_author(ctx)

    players = [starter]
    player_rolls = {}

    def needs_to_roll(name):
        return name in players and name not in player_rolls

    @bot.command(pass_context=True)
    async def join(ctx):
        """Allows the user to join the current game"""
        player = get_author(ctx)
        if player not in players:
            players.append(player)
            await bot.say('{} joined the game.'.format(get_name(player)))
        else:
            await bot.say('{} is already in the game.'.format(get_name(player)))

    await bot.say("Starting new {} roll. Type /join in the next 15 seconds to join.".format(mode))
    await asyncio.sleep(3.0)

    # if len(players) < 2:
    #     await bot.say('Not enough players.')
    #     await bot.remove_command('join')
    #     return

    bot.remove_command('join')

    async def normal(bet):
        """Begins a normal game with the specified bet. In normal games, everyone rolls 1-100 and the lowest roller owes
        the highest rolled the total amount betted."""
        await bot.say("Starting normal roll with {}g bet.".format(bet))

        while len(players) > len(player_rolls):
            await bot.wait_for_message(content='/roll')
            if last_roll[0].roller in players and last_roll[0].roller not in player_rolls:
                player_rolls[last_roll[0].roller] = last_roll[0].rolled
            await asyncio.sleep(1.0)

        winner = await determine(player_rolls,True)
        loser = await determine(player_rolls,False)

        await bot.say("{} owes {} {}g".format(get_name(loser), get_name(winner), bet))

    async def difference(bet):
        """Begins a difference game with the specified bet. In difference games, everyone rolls 1-bet and the lowest
        roller owes the highest roller the difference between their rolls."""
        await bot.say("Starting difference roll with {}g bet.".format(bet))

        while len(players) > len(player_rolls):
            if bet == 100:
                await bot.wait_for_message(content='/roll')
            else:
                await bot.wait_for_message(content='/roll {}'.format(bet))
            if last_roll[0].roller in players and last_roll[0].roller not in player_rolls:
                player_rolls[last_roll[0].roller] = last_roll[0].rolled
            await asyncio.sleep(1.0)

        winner = await determine(player_rolls, True)
        loser = await determine(player_rolls, False)
        the_difference = player_rolls[winner] - player_rolls[loser]

        await bot.say("{} owes {} {}g".format(get_name(loser), get_name(winner), the_difference))

    async def countdown(bet):
        """Starts a countdown game with the specified bet. In countdown games, the starter rolls 1-bet then everyone
        takes turns rolling 1-previous roll until somebody rolls 1 and loses. The winners receive the bet, evenly split
        among everyone."""
        await bot.say("Starting countdown roll with {}g bet.".format(bet))

        last_roll[0] = Roll(bet,None,bet)
        loser = None
        while last_roll[0].rolled > 1:
            for player in players:
                await asyncio.sleep(1.0)
                await bot.say('Waiting for roll to {} from {}'.format(last_roll[0].rolled, get_name(player)))
                if last_roll[0].rolled == 1:
                    loser = player
                    break
                elif last_roll[0].rolled == 100:
                    await bot.wait_for_message(content='/roll',author=player)
                else:
                    await bot.wait_for_message(content='/roll {}'.format(last_roll[0].rolled), author=player)


        winners = []
        for player in players:
            if player is not loser:
                winners.append(get_name(player))
        owed = bet // len(winners)

        await bot.say("{} owes {} {}g".format(get_name(loser), ', '.join(winners), owed))

    if mode == 'normal':
        await normal(bet)
    elif mode == 'difference':
        await difference(bet)
    else:
        await countdown(bet)

bot.remove_command('help')


@bot.command(pass_context=True)
async def hammerbot(ctx):
    bot.remove_command('hammerbot')
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