import discord, random, asyncio
from discord.ext import commands
from Rollbot.game import Game

description = '''A bot to roll for users and provide rolling games.'''
bot = commands.Bot(command_prefix='/', description=description)
client = discord.Client()


class Roll:
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
    if bet < 1:
        await bot.say('1 is the minimum for bets.')
        return

    starter = get_author(ctx)




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




bot.run('MzUwMzU0OTQzMjQ2NTk4MTQ2.DIC1AA.rsimVu4-dQ5oVrffSu5P_lLmNJY')

