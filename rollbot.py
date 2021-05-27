import discord
from discord.ext import commands
from time import localtime, time, asctime

from Core.constants import *
from Managers.SessionManagers.Bots.blackjack_bot import BlackjackBot
from Managers.SessionManagers.Bots.bombtile_bot import BombtileBot
from Managers.SessionManagers.Bots.hammer_race_bot import HammerRaceBot
from Managers.SessionManagers.Bots.meso_plz_bot import MesoPlzBot
from Managers.SessionManagers.Bots.roll_game_bot import RollGameBot
from Managers.SessionManagers.Bots.scratch_card_bot import ScratchCardBot
from Managers.SessionManagers.Bots.slot_machine_bot import SlotMachineBot
from Managers.SessionManagers.game_initializer import SessionOptions
from Managers.channel_manager import ChannelManager
from Managers.local_data_manager import LocalDataManager
from Managers.remote_data_manager import RemoteDataManager
from Managers.statistics import StatisticsBot
from MesoPlz.meso_plz import MesoPlz
from RollGames.roll import Roll
from Slots.modes import *
from discordtoken import TOKEN

intents = discord.Intents.default()
intents.members = True
description = '''A bot to roll for users and provide rolling games.'''
bot = commands.Bot(command_prefix='/', description=description, intents=intents)
blackjack_bot = None
channel_manager = None
hammer_race_bot = None
slot_machine_bot = None
scratchcard_bot = None
rollgame_bot = None
bombtile_bot = None
mesoplz_bot = None
stats_bot = None


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('---------')
    initialize_modules()


def get_data_manager():
    # TODO: Local data manager no longer works with discord.py update
    try:
        return RemoteDataManager(bot)
    except:
        print("No connection to the database")
        return
        return LocalDataManager(bot)


def initialize_modules():
    global blackjack_bot
    global channel_manager
    global hammer_race_bot
    global slot_machine_bot
    global scratchcard_bot
    global rollgame_bot
    global bombtile_bot
    global mesoplz_bot
    global stats_bot

    data_manager = get_data_manager()
    channel_manager = ChannelManager(bot)
    session_options = SessionOptions(bot, channel_manager, data_manager)

    blackjack_bot = BlackjackBot(session_options)
    hammer_race_bot = HammerRaceBot(session_options)
    slot_machine_bot = SlotMachineBot(session_options)
    scratchcard_bot = ScratchCardBot(session_options)
    rollgame_bot = RollGameBot(session_options)
    bombtile_bot = BombtileBot(session_options)
    mesoplz_bot = MesoPlzBot(session_options)
    stats_bot = StatisticsBot(bot, data_manager)


@bot.command()
async def roll(ctx, max=100):
    """Rolls a random integer between 1 and max. 100 is the default max if another is not given."""
    roller = ctx.message.author

    if max < 1:
        await ctx.send('1 is the minimum for rolls.')
        return

    roll = random.randint(1, max)

    try:
        channel = ctx.message.channel
        game = channel_manager.get_game(channel)
        await game.add_roll(Roll(roll, roller, max))
    except AttributeError:
        print("Existing game is not accepting rolls.")

    await ctx.send(f"{roller.display_name} rolled {roll} (1-{max})")


@bot.group()
async def rollgame(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send("You must specify a type of roll game. Try `/rollgame normal`")


@rollgame.command()
async def normal(ctx, bet=100):
    await rollgame_bot.create_normal_roll(ctx, bet)


@rollgame.command()
async def difference(ctx, bet=100):
    await rollgame_bot.create_difference_roll(ctx, bet)


@rollgame.command()
async def countdown(ctx, bet=100):
    await rollgame_bot.create_countdown_roll(ctx, bet)


@bot.command()
async def join(ctx):
    """ Allows the user to join the channel's active game. """
    await channel_manager.check_valid_join(ctx)


@bot.command()
async def blackjack(ctx):
    await blackjack_bot.create_game(ctx)


@bot.command()
async def hit(ctx):
    await blackjack_bot.make_move(ctx, 'hit')


@bot.command()
async def stand(ctx):
    await blackjack_bot.make_move(ctx, 'stand')


@bot.command()
async def split(ctx):
    await blackjack_bot.make_move(ctx, 'split')


@bot.command()
async def doubledown(ctx):
    await blackjack_bot.make_move(ctx, 'doubledown')


# End Blackjack commands

@bot.command()
async def quit(ctx):
    """ TODO leave the current game """


@bot.command()
async def askhammer(ctx):
    # TODO: No longer works with discord.py update
    return
    await hammer_race_bot.create_classic_race(ctx)


@bot.command()
async def compare(ctx):
    # TODO: No longer works with discord.py update
    return
    await hammer_race_bot.create_comparison(ctx)


@bot.command()
async def versushammer(ctx):
    # TODO: No longer works with discord.py update
    return
    await hammer_race_bot.create_versus(ctx)


@bot.command()
async def forcestart(ctx):
    await channel_manager.check_valid_forcestart(ctx)


@bot.command()
async def addai(ctx):
    # Add an AI to the game. The game must implement add_ai() for this to work.
    await channel_manager.check_valid_add_ai(ctx)


@bot.command()
async def fill(ctx):
    # TODO Fill the remaining player slots with AI players.
    await channel_manager.check_valid_add_ai(ctx)


@bot.command()
async def butts(ctx):
    num_butts = random.randint(1, 20)
    butts_message = [':peach:' * num_butts]
    # TODO: No longer works with discord.py update
    # stats_bot.update_butts(ctx, num_butts)
    if num_butts > 1:
        butts_message.append(f'```{num_butts} Butts```')
    else:
        butts_message.append(f'```{num_butts} Butt```')
    await ctx.send(''.join(butts_message))


@bot.command()
async def totalbutts(ctx):
    # TODO: No longer works with discord.py update
    return
    await stats_bot.total_butts(ctx)


@bot.command()
async def globalbutts(ctx):
    # TODO: No longer works with discord.py/boto update
    return
    await stats_bot.global_butts(ctx)


@bot.command()
async def melons(ctx):
    num_melons = random.randint(0, 10) * 2
    # TODO: No longer works with discord.py/boto update
    # stats_bot.update_melons(ctx, num_melons)

    item = 'Melons' if num_melons > 1 else 'Melon'
    if num_melons > 0:
        await ctx.send(':melon:' * num_melons + f'```{num_melons} {item}```')
    else:
        await ctx.send('```No Melons```')


@bot.command()
async def eggplants(ctx):
    amount = random.randint(0, 20)
    # TODO: No longer works with discord.py/boto update
    # stats_bot.update_eggplants(ctx, amount)
    item = 'Eggplants' if amount > 1 else 'Eggplant'
    if amount > 0:
        await ctx.send(':eggplant:' * amount + f'```{amount} {item}```')
    else:
        await ctx.send('```No dongerinos```')


@bot.command()
async def fuqs(ctx):
    amount = random.randint(0, 20)
    # TODO: No longer works with discord.py/boto update
    # stats_bot.update_fuqs(ctx, amount)
    item = 'fuqs' if amount > 1 else 'fuq'
    if amount > 0:
        await ctx.send('<:dafuq:451983622140854277>' * amount + f'```{amount} {item} given```')
    else:
        await ctx.send('```No fuqs given```')


@bot.command()
async def ducks(ctx):
    possible_ducks = [
        '<:psyduck:425868255501090818>',
        '<:shinypsyduck:708533235205931019>',
        '<:psy:457036806089867264>',
        '<a:spinningpsyduck:708525558446948414>',
        '<a:psymygod:519687422142054400>',
        '<:psyparty:612166267448721428>',
        '<:psywoke:667904479164760074>',
        '<:psysly:667904478845992991>',
        '<a:notlikeaduckonfire:562446845608198144>',
        '<a:notlikeacoldduck:530210238587207691>'
    ]
    amount = random.randint(0, 20)
    output = []
    for i in range(amount):
        index = random.randint(0, len(possible_ducks) - 1)
        output.append(possible_ducks[index])
    item = 'ducks' if len(output) > 1 else 'duck'
    if amount > 0:
        await ctx.send(' '.join(output))
        await ctx.send(f'```{amount} {item}```')
    else:
        await ctx.send('```Psy?```')

@bot.command()
async def slots(ctx):
    await slot_machine_bot.initialize_slots(ctx)


@bot.command()
async def bigslots(ctx):
    await slot_machine_bot.initialize_bigslots(ctx)


@bot.command()
async def giantslots(ctx):
    await slot_machine_bot.initialize_giantslots(ctx)


@bot.command()
async def mapleslots(ctx):
    await slot_machine_bot.initialize_mapleslots(ctx)


@bot.command()
async def bigmapleslots(ctx):
    await slot_machine_bot.initialize_bigmapleslots(ctx)


@bot.command()
async def giantmapleslots(ctx):
    await slot_machine_bot.initialize_giantmapleslots(ctx)

@bot.command()
async def pokeslots(ctx):
    await slot_machine_bot.initialize_pokeslots(ctx)


@bot.command()
async def bigpokeslots(ctx):
    await slot_machine_bot.initialize_bigpokeslots(ctx)


@bot.command()
async def giantpokeslots(ctx):
    await slot_machine_bot.initialize_giantpokeslots(ctx)


@bot.command()
async def hammerpot(ctx):
    # TODO: No longer works with discord.py update
    return
    await scratchcard_bot.create_hammerpot(ctx)


@bot.command()
async def scratchcard(ctx):
    # TODO: No longer works with discord.py update
    return
    await scratchcard_bot.create_classic(ctx)


@bot.command()
async def pick(ctx):
    # TODO: No longer works with discord.py update
    return
    await scratchcard_bot.pick_line(ctx)


@bot.command()
async def scratch(ctx):
    # TODO: No longer works with discord.py update
    return
    await scratchcard_bot.scratch(ctx)


@bot.command()
async def scratchbutts(ctx):
    pick_random = random.randint(0, len(SCRATCH_BUTTS) - 1)
    message = ':peach:' + SCRATCH_BUTTS[pick_random]
    await ctx.send(message)


@bot.command()
async def mesoplz(ctx):
    await mesoplz_bot.mesos_plz(ctx)


@bot.command()
async def gold(ctx, query=None):
    await stats_bot.query_gold(ctx, query)


@bot.command()
async def gold_stats(ctx, query=None):
    # TODO: No longer works with discord.py update
    return
    await stats_bot.query_gold_stats(ctx, query)


@bot.command()
async def winnings(ctx, query=None):
    # TODO: No longer works with discord.py update
    await stats_bot.query_winnings(ctx, query)


@bot.command()
async def losses(ctx, query=None):
    # TODO: No longer works with discord.py update
    await stats_bot.query_losses(ctx, query)


@bot.command()
async def flip(ctx):
    await bombtile_bot.flip(ctx)


@bot.command()
async def bombtile(ctx):
    await bombtile_bot.create_bombtile(ctx)


bot.remove_command('help')


@bot.group()
async def help(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send(BASIC_COMMANDS)


@help.command()
async def slots(ctx):
    await ctx.send(SLOTS_COMMANDS)


@help.command()
async def blackjack(ctx):
    await ctx.send(BLACKJACK_COMMANDS)


@help.command()
async def rollgame(ctx):
    await ctx.send(ROLLGAME_COMMANDS)


@help.command()
async def scratchcard(ctx):
    await ctx.send(SCRATCHCARD_COMMANDS)


@help.command()
async def hammerrace(ctx):
    await ctx.send(HAMMERRACE_COMMANDS)


@bot.command(aliases=['8ball'])
async def eightball(ctx):
    pick_random = random.randint(0, len(EIGHTBALL_RESPONSES) - 1)
    await ctx.send(EIGHTBALL_RESPONSES[pick_random])


def main():
    try:
        bot.run(TOKEN)
    finally:
        print(f'End running at {asctime(localtime(time()))}')


if __name__ == '__main__':
    main()
