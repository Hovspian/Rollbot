import discord
import random
import asyncio
from discord.ext import commands
from RollGames.game import Game, last_roll
from RollGames.roll import Roll
from HammerRace.hammer_modes import *
from discordtoken import TOKEN
from Slots.slots import SlotMachine
from constants import *
from channel_manager import ChannelManager

description = '''A bot to roll for users and provide rolling games.'''
bot = commands.Bot(command_prefix='/', description=description)
client = discord.Client()
channel_manager = ChannelManager()


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('-' * len(bot.user.id))


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

    if channel_manager.is_game_in_progress(channel):
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
    channel_manager.add_game_in_progress(channel, the_game)
    await the_game.play()
    channel_manager.remove_channel(channel)


@bot.command(pass_context=True)
async def join(ctx):
    """Allows the user to join the current game"""
    channel = ctx.message.channel
    author = ctx.message.author
    error = channel_manager.is_invalid_user_error(channel, author)

    if error:
        await bot.say(error)
    else:
        await channel_manager.add_user_to_game(channel, author)
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


@bot.command(pass_context=True)
async def butts(ctx):
    message = ctx.message
    tich = discord.utils.get(message.server.members, name = "Tich Showers")
    num_butts = random.randint(1, 20)
    # await bot.say(tich.mention)
    await bot.say(':peach:' * num_butts)
    if num_butts == 1:
        await bot.say('```{} Butt```'.format(num_butts))
    else:
        await bot.say('```{} Butts```'.format(num_butts))


@bot.command(pass_context=True)
async def slots(ctx):
    author = ctx.message.author
    slot_machine = SlotMachine(author.display_name)
    await bot.say(slot_machine.play_slot())

bot.remove_command('help')


@bot.command()
async def help():
    await bot.say(ROLLBOT_COMMANDS)


@bot.command(alias='8ball')
async def eightball():
    pick = random.randint(0, len(EIGHTBALL_RESPONSES) - 1)
    await bot.say(EIGHTBALL_RESPONSES[pick])


bot.run(TOKEN)
