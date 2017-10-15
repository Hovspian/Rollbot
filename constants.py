EIGHTBALL_RESPONSES = ['It is certain',
                       'It is decidedly so',
                       'Without a doubt',
                       'Yes definitely',
                       'You may rely on it',
                       'As I see it, yes',
                       'Most likely',
                       'Outlook good',
                       'Yes',
                       'Signs point to yes',
                       'Reply hazy try again',
                       'Ask again later',
                       'Better not tell you now',
                       'Cannot predict now',
                       'Concentrate and ask again',
                       'Don\'t count on it',
                       'My reply is no',
                       'My sources say no',
                       'Outlook not so good',
                       'Very doubtful']

ROLLBOT_COMMANDS = "```Rollbot commands: " \
                   "\n   /roll <max> - Rolls a random number between 1 and max. 100 is the default max. " \
                   "\n   /start <mode> <bet> - Starts a new game. The bet is set to 100 if not specified. " \
                   "\n   Note: only one game can be in progress at a time. " \
                   "\n   /join - Join the current game. " \
                   "\n\nGame modes: " \
                   "\n   normal - everyone rolls 1-100. The lowest roller owes the highest roller the bet. " \
                   "\n   difference - everyone rolls 1-bet and the lowest roller owes the highest roller " \
                   "the difference between the rolls." \
                   "\n   countdown - the starter rolls 1-bet then everyone takes turns rolling 1-previous" \
                   " roll until someone rolls 1 and loses. The winnings are split between everyone else. " \
                   "\n   Note: if there is a tie then I will do more rolls on my own to decide the winner```"

SPACE = ' '
DOUBLE_SPACE = '  '
CODE_TAG = '```'
LINEBREAK = '\n'
