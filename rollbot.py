import discord
from discord.ext import commands

from GridGames.Slots.modes import *
from Managers.channel_manager import ChannelManager
from Managers.data_manager import SessionDataManager
from Managers.session_manager import SessionManager
from Managers.statistics import StatisticsBot
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
blackjack_bot = session_manager.blackjack_bot
scratch_card_bot = session_manager.scratch_card_bot
data_manager = SessionDataManager()
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
    channel_manager.add_game_in_session(channel, the_game)
    await the_game.play()
    channel_manager.vacate_channel(channel)


@bot.command(pass_context=True)
async def join(ctx):
    """ Allows the user to join the current game """
    await session_manager.join_game(ctx)


# Blackjack commands

@bot.command(pass_context=True)
async def blackjackhelp():
    options = ["Blackjack commands:",
               "`/hit` : Receive a card. If your hand's value exceeds 21 points, it's a bust.",
               "`/stand` : End your turn with your hand as-is.",
               "`/doubledown` : Double your wager, receive one more card, and stand.",
               "`/split` : If you are dealt two cards of equal value, split them into separate hands."]
    await bot.say(LINEBREAK.join(options))


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
    await scratch_card_bot.make_action(ctx, "pick")


@bot.command(pass_context=True)
async def scratch(ctx):
    await scratch_card_bot.make_action(ctx, "scratch")


@bot.command(pass_context=True)
async def gold(ctx):
    await stats_bot.query_gold(ctx)


bot.remove_command('help')


@bot.command()
async def help():
    await bot.say(ROLLBOT_COMMANDS)


@bot.command(alias='8ball')
async def eightball():
    pick_random = random.randint(0, len(EIGHTBALL_RESPONSES) - 1)
    await bot.say(EIGHTBALL_RESPONSES[pick_random])


bot.run(TOKEN)
