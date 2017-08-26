# Rollbot
A discord bot using discord.py.
Allows users to roll and provides rolling games.


Rollbot commands:

    /help - Displays a message providing information about the bot and its commands.
    /roll <max> - Rolls a random number between 1 and max. 100 is the default max.
    /start <mode> <bet> - Starts a new game. The bet is set to 100 if not specified.
    Note: only one game can be in progress at a time.
    /join - Join the current game.
   
Game modes:

    normal - everyone rolls 1-100. The lowest roller owes the highest roller the bet.
    difference - everyone rolls 1-bet and the lowest roller owes the highest roller the difference between the rolls.
    countdown - the starter rolls 1-bet, then everyone takes turns rolling 1-previous roll until someone rolls 1 and
    loses. The winnings are split between everyone else.
    Note: the bot does rerolls on its own in the case of a tie.
