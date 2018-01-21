import discord
from discord.ext import commands

from Core.constants import *
from Managers.SessionManagers.blackjack_bot import BlackjackBot
from Managers.SessionManagers.game_initializer import SessionOptions
from Managers.SessionManagers.hammer_race_bot import HammerRaceBot
from Managers.SessionManagers.roll_game_bot import RollGameBot
from Managers.SessionManagers.scratch_card_bot import ScratchCardBot
from Managers.SessionManagers.slot_machine_bot import SlotMachineBot
from Managers.channel_manager import ChannelManager
from Managers.data_manager import SessionDataManager
from Managers.statistics import StatisticsBot
from RollGames.roll import Roll
from Slots.modes import *
from discordtoken import TOKEN

description = '''A bot to roll for users and provide rolling games.'''
bot = commands.Bot(command_prefix='&', description=description)
client = discord.Client()
data_manager = SessionDataManager()
channel_manager = ChannelManager(bot)
session_options = SessionOptions(bot, channel_manager, data_manager)
blackjack_bot = BlackjackBot(session_options)
hammer_race_bot = HammerRaceBot(session_options)
slot_machine_bot = SlotMachineBot(session_options)
scratchcard_bot = ScratchCardBot(session_options)
rollgame_bot = RollGameBot(session_options)
stats_bot = StatisticsBot(bot, data_manager)


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
    await bot.say(f"{roller.display_name} rolled {roll} (1-{max})")

    try:
        game = channel_manager.get_game(ctx)
        await game.add_roll(Roll(roll, roller, max))
    except AttributeError:
        pass


@bot.group(pass_context=True)
async def rollgame(ctx):
    if ctx.invoked_subcommand is None:
        await bot.say("You must specify a type of roll game. Try `/rollgame normal`")


@rollgame.command(pass_context=True)
async def normal(ctx, bet=100):
    await rollgame_bot.create_normal_roll(ctx, bet)


@rollgame.command(pass_context=True)
async def difference(ctx, bet=100):
    await rollgame_bot.create_difference_roll(ctx, bet)


@rollgame.command(pass_context=True)
async def countdown(ctx, bet=100):
    await rollgame_bot.create_countdown_roll(ctx, bet)

"""
Allows the user to join the channel's active game.
"""
@bot.command(pass_context=True)
async def join(ctx):
    await channel_manager.check_valid_join(ctx)


@bot.command(pass_context=True)
async def blackjack(ctx):
    await blackjack_bot.create_game(ctx)


@bot.command(pass_context=True)
async def hit(ctx):
    await blackjack_bot.make_move(ctx, 'hit')


@bot.command(pass_context=True)
async def stand(ctx):
    await blackjack_bot.make_move(ctx, 'stand')


@bot.command(pass_context=True)
async def split(ctx):
    await blackjack_bot.make_move(ctx, 'split')


@bot.command(pass_context=True)
async def doubledown(ctx):
    await blackjack_bot.make_move(ctx, 'doubledown')


# End Blackjack commands

@bot.command(pass_context=True)
async def quit(ctx):
    """ TODO leave the current game """


@bot.command(pass_context=True)
async def askhammer(ctx):
    await hammer_race_bot.create_classic_race(ctx)


@bot.command(pass_context=True)
async def compare(ctx):
    await hammer_race_bot.create_comparison(ctx)


@bot.command(pass_context=True)
async def versushammer(ctx):
    await hammer_race_bot.create_versus(ctx)


@bot.command(pass_context=True)
async def forcestart(ctx):
    pass

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
    await slot_machine_bot.initialize_slots(ctx)


@bot.command(pass_context=True)
async def bigslots(ctx):
    await slot_machine_bot.initialize_bigslots(ctx)


@bot.command(pass_context=True)
async def giantslots(ctx):
    await slot_machine_bot.initialize_giantslots(ctx)


@bot.command(pass_context=True)
async def mapleslots(ctx):
    await slot_machine_bot.initialize_mapleslots(ctx)


@bot.command(pass_context=True)
async def bigmapleslots(ctx):
    await slot_machine_bot.initialize_bigmapleslots(ctx)


@bot.command(pass_context=True)
async def giantmapleslots(ctx):
    await slot_machine_bot.initialize_giantmapleslots(ctx)


@bot.command(pass_context=True)
async def hammerpot(ctx):
    await scratchcard_bot.create_hammerpot(ctx)


@bot.command(pass_context=True)
async def scratchcard(ctx):
    await scratchcard_bot.create_classic(ctx)


@bot.command(pass_context=True)
async def pick(ctx):
    await scratchcard_bot.pick_line(ctx)


@bot.command(pass_context=True)
async def scratch(ctx):
    await scratchcard_bot.scratch(ctx)


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
