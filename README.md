# Rollbot
A discord bot using discord.py.

Allows users to play games of chance.

## Features
- Blackjack
- Slots
- Roll games
- Scratch cards
- Hammer race
- Magic 8 ball


### Rollbot commands:
`/help <type>` - Gives users information about Rollbot commands for different features. Gives the general commands if no type is given.

Types: blackjack, slots, rollgame, scratchcard, hammerrace

`/gold <user>` - Says how much gold a particular user has earned/lost in total. Returns the caller's information if no user is given

`/join` - Join the current game if one is available

`/roll <max>` - Roll a random number between 1 and max. The max defaults 100 if none is given

`/eightball <question>` - Ask a question to the magic 8 ball

   
### Blackjack commands:
`/blackjack` - Start a new blackjack game

`/hit` - Receive a card. If your hand's value exceeds 21 points, it's a bust

`/stand` - End your turn with your hand as-is

`/doubledown` - Double your wager, receive one more card, and stand

`/split` - If you are dealt two cards of equal value, split them into separate hands

### Slots commands:
`/slots` - Play a 3x3 slot machine

`/bigslots` - Play a 5x5 slot machine

`/giantslots` - Play a 7x7 slot machine

`/mapleslots` - Play a 3x3 slot machine using maple icons

`/bigmapleslots` - Play a 5x5 slot machine using maple icons

`/giantmapleslots` - Play a 7x7 slot machine using maple icons

### Roll game commands:
`/rollgame <mode>` - Starts a new roll game

Modes: normal, difference, and countdown

`normal` - Everyone rolls 1-100. The lowest roller owes the highest roller the bet

`difference` - Everyone rolls 1-bet and the lowest roller owes the highest roller the difference between their rolls

`countdown` - The starter rolls 1-bet then everyone takes turns rolling 1-previous roll until someone rolls 1 and loses. The winnings are split between everyone else

If there is a tie then the bot will do more rolls on its own to determine the winner.


### Scratch card commands:
`/scratchcard` - Creates a new scratch card for the user

`/hammerpot` - Creates a new hammer pot for the user

`/scratch <space>` - Scratches off the specified space. The user can also specify multiple spaces at once by separating them with commas.

`/pick <line>` - Pick a row, column, or diagonal to use for hammerpot

### Hammer race commands:

`/versushammer` - Creates a joinable hammer race

`/askhammer` - Ask a question and get a yes, no, or hammer response

`/compare <entry 1, entry 2, ..., entry 5>` - Creates a hammer race comparing 2-5 entries






