import asyncio
import discord
from discord.ext import commands
from GridGames.Slots.modes import *
from HammerRace.hammer_modes import *
from Managers.channel_manager import ChannelManager
from Managers.session_manager import SessionManager
from RollGames.roll import Roll
from RollGames.rollgame import RollGame, last_roll
from constants import *
from discordtoken import TOKEN
from helper_functions import *

description = '''A bot to roll for users and provide rolling games.'''
bot = commands.Bot(command_prefix='/', description=description)
client = discord.Client()
channel_manager = ChannelManager(bot)
session_manager = SessionManager(bot)


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

    the_game = RollGame(bot, mode, bet, channel)
    await the_game.add(starter)
    channel_manager.add_game_in_progress(channel, the_game)
    await the_game.play()
    channel_manager.vacate_channel(channel)


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
        await bot.say("{} joined the game.".format(author))


@bot.command(pass_context=True)
async def askhammer(ctx):
    await session_manager.create_askhammer(ctx)


@bot.command(pass_context=True)
async def testcompare(ctx):
    await session_manager.create_comparisonhammer(ctx)


@bot.command(pass_context=True)
async def versushammer(ctx):
    await session_manager.create_versushammer(ctx)


@bot.command(pass_context=True)
async def butts():
    num_butts = random.randint(1, 20)
    butts_message = [':peach:' * num_butts]
    if num_butts > 1:
        butts_message.append(f'```{num_butts} Butts```')
    else:
        butts_message.append(f'```{num_butts} Butt```')
    await bot.say(''.join(butts_message))


@bot.command(pass_context=True)
async def slots(ctx):
    await play_slots(ctx, slot_machine=ClassicSlots())


@bot.command(pass_context=True)
async def bigslots(ctx):
    await play_slots(ctx, slot_machine=BigClassicSlots())


@bot.command(pass_context=True)
async def giantslots(ctx):
    await play_slots(ctx, slot_machine=GiantClassicSlots())


@bot.command(pass_context=True)
async def mapleslots(ctx):
    await play_slots(ctx, slot_machine=MapleSlots())


@bot.command(pass_context=True)
async def bigmapleslots(ctx):
    await play_slots(ctx, slot_machine=BigMapleSlots())


@bot.command(pass_context=True)
async def giantmapleslots(ctx):
    await play_slots(ctx, slot_machine=GiantMapleSlots())


async def play_slots(ctx, slot_machine):
    author = ctx.message.author.display_name
    slot_machine.play_slot()
    report = '\n'.join([f"{author}'s slot results", slot_machine.get_outcome_report()])
    await bot.say(slot_machine.draw_slot_interface())
    await bot.say(report)


@bot.command(pass_context=True)
async def hammerpot(ctx):
    await session_manager.create_hammerpot(ctx)


@bot.command(pass_context=True)
async def scratchcard(ctx):
    await session_manager.create_scratch_card(ctx)


@bot.command(pass_context=True)
async def pick(ctx):
    await session_manager.pick_line(ctx)


@bot.command(pass_context=True)
async def scratch(ctx):
    await session_manager.scratch(ctx)


bot.remove_command('help')


@bot.command()
async def help():
    await bot.say(ROLLBOT_COMMANDS)


@bot.command(alias='8ball')
async def eightball():
    pick_random = random.randint(0, len(EIGHTBALL_RESPONSES) - 1)
    await bot.say(EIGHTBALL_RESPONSES[pick_random])


bot.run(TOKEN)
