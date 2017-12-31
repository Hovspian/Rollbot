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
`/help <type>` - a more specific help command for different game types

Types: blackjack, slots, rollgame, scratchcard, hammerrace

`/gold <user>` - says how much gold a particular user has earned/lost in total. Returns the caller's information if no user is given

`/join` - join the current game if one is available

`/roll <max>` - Roll a random number between 1 and max. The max defaults 100 if none is given

`/eightball <question>` - ask a question to the magic 8 ball

   
### Blackjack commands:
`/blackjack` - start a new blackjack game

`/hit` - Receive a card. If your hand's value exceeds 21 points, it's a bust

`/stand` - End your turn with your hand as-is

`/doubledown` - Double your wager, receive one more card, and stand

`/split` - If you are dealt two cards of equal value, split them into separate hands

### Slots commands:
`/slots` - play a 3x3 slot machine

`/bigslots` - play a 5x5 slot machine

`/giantslots` - play a 7x7 slot machine

`/mapleslots` - play a 3x3 slot machine using maple icons

`/bigmapleslots` - play a 5x5 slot machine using maple icons

`/giantmapleslots` - play a 7x7 slot machine using maple icons

### Rollgame commands:
`/rollgame <mode>` - Starts a new roll game

Modes: normal, difference, and countdown

`normal` - everyone rolls 1-100. The lowest roller owes the highest roller the bet

`difference` - everyone rolls 1-bet and the lowest roller owes the highest roller the difference between their rolls

`countdown` - the starter rolls 1-bet then everyone takes turns rolling 1-previous roll until someone rolls 1 and loses. The winnings are split between everyone else

If there is a tie then the bot will do more rolls on its own to determine the winner.













