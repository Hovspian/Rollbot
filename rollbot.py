import asyncio

import discord
from discord.ext import commands

from GridGames.Slots.modes import *
from HammerRace.hammer_modes import *
from Managers.channel_manager import ChannelManager
from Managers.scratch_card_bot import ScratchCardBot
from RollGames.roll import Roll
from RollGames.rollgame import RollGame, last_roll
from constants import *
from discordtoken import TOKEN

description = '''A bot to roll for users and provide rolling games.'''
bot = commands.Bot(command_prefix='/', description=description)
client = discord.Client()
channel_manager = ChannelManager(bot)
scratch_card_bot = ScratchCardBot(bot)


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
async def compare(ctx):
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
        await bot.say("Please enter 2-5 options, separated by commas. Example: ```/compare bread, eggs, hammer```")


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


@bot.group(name='new', pass_context=True)
async def new(ctx):
    if ctx.invoked_subcommand is None:
        pass
        # TODO
    pass

@new.command(pass_context=True)
async def hammerpot(ctx):
    if await is_valid_new_game(ctx, scratch_card_bot):
        hammerpot = await scratch_card_bot.create_hammerpot(ctx)
        channel_manager.add_game_in_progress(ctx, hammerpot)
        game_ended = await scratch_card_bot.set_time_limit(hammerpot)
        if game_ended:
            channel_manager.vacate_channel(ctx)


@new.command(pass_context=True)
async def scratchcard(ctx):
    if await is_valid_new_game(ctx, scratch_card_bot):
        scratch_card = await scratch_card_bot.create_scratch_card(ctx)
        channel_manager.add_game_in_progress(ctx, scratch_card)
        game_ended = await scratch_card_bot.set_time_limit(scratch_card)
        if game_ended:
            channel_manager.vacate_channel(ctx)


@bot.command(pass_context=True)
async def pick(ctx):
    valid_channel_host = await channel_manager.is_valid_channel_host(ctx)
    game = await scratch_card_bot.get_game(ctx)
    if valid_channel_host and game:
        raw_input = message_without_command(ctx.message.content)
        await scratch_card_bot.pick_line(game, raw_input)


@bot.command(pass_context=True)
async def scratch(ctx):
    valid_channel_host = await channel_manager.is_valid_channel_host(ctx)
    game = await scratch_card_bot.get_game(ctx)
    if valid_channel_host and game:
        raw_input = message_without_command(ctx.message.content)
        await scratch_card_bot.next_turn(game, raw_input)


async def is_valid_new_game(ctx, game_manager) -> bool:
    # Check channel and game manager
    host = ctx.message.author
    valid_channel = await channel_manager.check_valid_new_game(ctx)
    valid_user = await game_manager.check_valid_user(host)
    return valid_channel and valid_user


bot.remove_command('help')


@bot.command()
async def help():
    await bot.say(ROLLBOT_COMMANDS)


@bot.command(alias='8ball')
async def eightball():
    pick = random.randint(0, len(EIGHTBALL_RESPONSES) - 1)
    await bot.say(EIGHTBALL_RESPONSES[pick])


bot.run(TOKEN)
