import discord
import random
import asyncio
from discord.ext import commands
from RollGames.game import Game, last_roll
from RollGames.roll import Roll
from HammerRace.hammer_modes import *
from discordtoken import TOKEN
from constants import *

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
    last_roll[0] = Roll(roll, roller, max)
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
    if not game_in_channel(channel):
        await bot.say("No game in this channel")
    elif games_in_progress[channel].in_progress:
        await bot.say("It's too late to join.")
    elif game_in_channel(channel) and person_in_game(author, channel):
        await bot.say("{} is already in the game.".format(author.display_name))
    else:
        await games_in_progress[channel].add(author)
        await bot.say("{} joined the game.".format(author.display_name))


def game_in_channel(channel):
    return channel in games_in_progress.keys()


def person_in_game(person, channel):
    return person in games_in_progress[channel].players


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
        await bot.say(question + ':')

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

        await bot.say('Out of ' + options + ':\n' + hammer_manager.winner_report())
    else:
        await bot.say("Please enter 2-5 options, separated by commas. Example: ```/hammer bread, eggs, hammer```")


bot.remove_command('help')


@bot.command()
async def help():
    await bot.say(ROLLBOT_COMMANDS)


@bot.command(alias='8ball')
async def eightball():
    pick = random.randint(0, len(EIGHTBALL_RESPONSES) - 1)
    await bot.say(EIGHTBALL_RESPONSES[pick])


bot.run(TOKEN)
