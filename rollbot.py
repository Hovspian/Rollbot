
import discord, random, asyncio
from discord.ext import commands
from game import Game, last_roll
from roll import Roll
import discord
import random
import asyncio
import math
import discordtoken
from discord.ext import commands
from HammerRace.hammerbot import *

description = '''A bot to roll for users and provide rolling games.'''
bot = commands.Bot(command_prefix='/', description=description)
client = discord.Client()


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('-' * len(bot.user.id))



games_in_progress = {}

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
    return last_roll[0]


@bot.command(pass_context=True)
async def start(ctx, mode: str, bet=100):
    """Starts the game mode specified with the given bet. If no bet is given, 100 is chosen as the default."""
    starter = ctx.message.author
    channel = ctx.message.channel
    valid_modes = ['normal', 'difference', 'countdown']

    if channel in games_in_progress.keys():
        await bot.say('Game already in progress in channel')
        return
    if mode not in valid_modes:
        await bot.say('Invalid game mode.')
        return
    if bet < 1:
        await bot.say('1 is the minimum for bets.')
        return

    the_game = Game(bot, mode, bet, channel)
    await the_game.add(starter)
    games_in_progress[channel] = the_game
    await the_game.play()
    games_in_progress.pop(channel)


@bot.command(pass_context=True)
async def join(ctx):
    """Allows the user to join the current game"""
    channel = ctx.message.channel
    author = ctx.message.author
    if channel not in games_in_progress.keys():
        await bot.say("No game in this channel")
        return
    elif channel in games_in_progress.keys() and author in games_in_progress[channel].players:
        await bot.say("{} is already in the game.".format(author.display_name))
        return
    else:
        games_in_progress[channel].add(author)
        await bot.say("{} joined the game.".format(author.display_name))


def message_without_command(full_string):
    command, space, message_body = str(full_string).partition(' ')
    return message_body


@bot.command(pass_context=True)
async def askhammer(ctx):
    question = message_without_command(ctx.message.content)
    hammer_manager = ClassicHammer()
    await bot.say(hammer_manager.round_report())

    while hammer_manager.race_in_progress:
        await asyncio.sleep(2.0)
        hammer_manager.next_round()
        await bot.say(hammer_manager.round_report())

    if question != '':
        await bot.say('"' + question + '":')

    await bot.say(hammer_manager.winner_report())


@bot.command(pass_context=True)
async def hammer(ctx):
    options = message_without_command(ctx.message.content)
    hammer_manager = ComparisonHammer(options)

    if hammer_manager.valid_num_participants():
        await bot.say(hammer_manager.round_report())

        while hammer_manager.race_in_progress:
            await asyncio.sleep(2.0)
            hammer_manager.next_round()
            await bot.say(hammer_manager.round_report())

        await bot.say(options + ':\n' + hammer_manager.winner_report())
    else:
        await bot.say("Please enter 2-5 options, separated by commas. Example: \n ```/hammer bread, eggs, hammer```")


@bot.command(pass_context=True)
async def hammerrace(ctx):
    """TODO"""


bot.remove_command('help')


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


bot.run(discordtoken.TOKEN)

