import discord
from discord.ext import commands

from GridGames.Slots.modes import *
from Managers.channel_manager import ChannelManager
from Managers.data_manager import SessionDataManager
from Managers.session_manager import SessionManager
from Managers.statistics import StatisticsBot
from Managers.GameManagers.slot_machine_bot import SlotMachineBot
from Managers.GameManagers.roll_game_bot import RollGameBot
from RollGames.roll import Roll
from RollGames.rollgame import RollGame
from RollGames.roll_game_modes import NormalRollGame
from constants import *
from discordtoken import TOKEN
from helper_functions import *

description = '''A bot to roll for users and provide rolling games.'''
bot = commands.Bot(command_prefix='/', description=description)
client = discord.Client()
data_manager = SessionDataManager()
session_manager = SessionManager(bot)
channel_manager = session_manager.channel_manager
blackjack_bot = session_manager.blackjack_bot
scratch_card_bot = session_manager.scratch_card_bot
stats_bot = StatisticsBot(bot, data_manager)
slot_machine_bot = SlotMachineBot(bot, data_manager)
roll_game_bot = session_manager.roll_game_bot


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

    try:
        game = channel_manager.get_game(ctx)
        game.last_roll[0] = Roll(roll, roller, max)
    except:
        pass
    await bot.say(f"{roller.display_name} rolled {roll} (1-{max})")


@bot.group(pass_context=True)
async def rollgame(ctx):
    if ctx.invoked_subcommand is None:
        await bot.say("You must specify a type of roll game. Try `/rollgame normal`")


@rollgame.command(pass_context=True)
async def normal(ctx, bet = 100):
    await session_manager.create_normal_rollgame(ctx, bet)


@rollgame.command(pass_context=True)
async def difference(ctx, bet = 100):
    await session_manager.create_difference_rollgame(ctx, bet)


@rollgame.command(pass_context=True)
async def countdown(ctx, bet = 100):
    await session_manager.create_countdown_rollgame(ctx, bet)


@bot.command(pass_context=True)
async def join(ctx):
    """ Allows the user to join the current game """
    await session_manager.join_game(ctx)


# Blackjack commands


@bot.command(pass_context=True)
async def blackjack(ctx):
    await session_manager.create_blackjack(ctx)


@bot.command(pass_context=True)
async def hit(ctx):
    await blackjack_bot.perform_action(ctx, "hit")


@bot.command(pass_context=True)
async def stand(ctx):
    await blackjack_bot.perform_action(ctx, "stand")


@bot.command(pass_context=True)
async def split(ctx):
    await blackjack_bot.perform_action(ctx, "split")


@bot.command(pass_context=True)
async def doubledown(ctx):
    await blackjack_bot.perform_action(ctx, "doubledown")


# End Blackjack commands

@bot.command(pass_context=True)
async def quit(ctx):
    """ TODO leave the current game """


@bot.command(pass_context=True)
async def askhammer(ctx):
    await session_manager.askhammer(ctx)


@bot.command(pass_context=True)
async def compare(ctx):
    await session_manager.comparison_hammer(ctx)


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
    await slot_machine_bot.play_slots(ClassicSlots(ctx))


@bot.command(pass_context=True)
async def bigslots(ctx):
    await slot_machine_bot.play_slots(BigClassicSlots(ctx))


@bot.command(pass_context=True)
async def giantslots(ctx):
    await slot_machine_bot.play_slots(GiantClassicSlots(ctx))


@bot.command(pass_context=True)
async def mapleslots(ctx):
    await slot_machine_bot.play_slots(MapleSlots(ctx))


@bot.command(pass_context=True)
async def bigmapleslots(ctx):
    await slot_machine_bot.play_slots(BigMapleSlots(ctx))


@bot.command(pass_context=True)
async def giantmapleslots(ctx):
    await slot_machine_bot.play_slots(GiantMapleSlots(ctx))


@bot.command(pass_context=True)
async def hammerpot(ctx):
    await session_manager.create_hammerpot(ctx)


@bot.command(pass_context=True)
async def scratchcard(ctx):
    await session_manager.create_scratch_card(ctx)


@bot.command(pass_context=True)
async def pick(ctx):
    await scratch_card_bot.make_action(ctx, "pick")


@bot.command(pass_context=True)
async def scratch(ctx):
    await scratch_card_bot.make_action(ctx, "scratch")


@bot.command(pass_context=True)
async def gold(ctx):
    await stats_bot.query_gold(ctx)


bot.remove_command('help')


@bot.group(pass_context = True)
async def help(ctx):
    if ctx.invoked_subcommand is None:
        await bot.say(BASIC_COMMANDS)


@help.command()
async def slots():
    await bot.say(SLOTS_COMMANDS)


@help.command()
async def blackjack():
    await bot.say(BLACKJACK_COMMANDS)


@help.command()
async def rollgame():
    await bot.say(ROLLGAME_COMMANDS)


@help.command()
async def scratchcard():
    await bot.say(SCRATCHCARD_COMMANDS)


@help.command()
async def hammerrace():
    await bot.say(HAMMERRACE_COMMANDS)


@bot.command(alias='8ball')
async def eightball():
    pick_random = random.randint(0, len(EIGHTBALL_RESPONSES) - 1)
    await bot.say(EIGHTBALL_RESPONSES[pick_random])


bot.run(TOKEN)
