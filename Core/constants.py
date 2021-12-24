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

BASIC_COMMANDS = "**Rollbot commands:**" \
                 "\n`/gold` - says how much gold you've earned/lost in total" \
                 "\n`/gold <user>` - says how much gold a particular person has earned/lost" \
                 "\n`/join` - join the current game if one is available" \
                 "\n`/butts` - gets a random number of butts between 1 and 20" \
                 "\n`/roll <max>` - Roll a random number between 1 and max. The max defaults 100 if none is given" \
                 "\n`/eightball <question>` - ask a question to the magic 8 ball" \
                 "\n`/help <type>` - a more specific help command for different game types" \
                 "\nTypes: slots, blackjack, rollgame, scratchcard, hammerrace"

SLOTS_COMMANDS = "**Slots commands:**" \
                 "\n`/slots` - play a 3x3 slot machine" \
                 "\n`/bigslots` - play a 5x5 slot machine" \
                 "\n`/giantslots` - play a 7x7 slot machine" \
                 "\n`/mapleslots` - play a 3x3 slot machine using maple icons" \
                 "\n`/bigmapleslots` - play a 5x5 slot machine using maple icons" \
                 "\n`/giantmapleslots` - play a 7x7 slot machine using maple icons"

BLACKJACK_COMMANDS = "**Blackjack commands:**" \
                     "\n`/blackjack` - start a new blackjack game" \
                     "\n`/hit` - Receive a card. If your hand's value exceeds 21 points, it's a bust." \
                     "\n`/stand` - End your turn with your hand as-is." \
                     "\n`/doubledown` - Double your wager, receive one more card, and stand." \
                     "\n`/split` - If you are dealt two cards of equal value, split them into separate hands."

SCRATCHCARD_COMMANDS = "**Scratch Card commands:**" \
                       "\n`/scratchcard` - Creates a new scratch card for the user" \
                       "\n`/hammerpot` - Creates a new hammer pot for the user" \
                       "\n`/scratch <space>` - Scratches off the specified space or spaces, separated by commas" \
                       "\n`/pick <line>` - Pick a row, column, or diagonal (hammerpot only)"

HAMMERRACE_COMMANDS = "**Hammer Race commands:**" \
                      "\n`/versushammer` - Creates a joinable hammer race" \
                      "\n`/askhammer` - Ask a question and get a yes, no, or hammer response" \
                      "\n`/compare <entry 1, entry 2, ..., entry 5>` - Creates a hammer race comparing 2-5 entries"

ROLLGAME_COMMANDS = "**Rollgame commands:**" \
                    "\n`/rollgame <mode> <bet>` - Starts a new roll game with the specified bet." \
                    "\nModes: normal, difference, and countdown" \
                    "\nThe bet will default to 100 if one isn't specified" \
                    "\n`normal` - everyone rolls 1-100. The lowest roller owes the highest roller the bet." \
                    "\n`difference` - everyone rolls 1-bet and the lowest roller owes the highest roller the " \
                    "difference between their rolls." \
                    "\n`countdown` - the starter rolls 1-bet then everyone takes turns rolling 1-previous roll until" \
                    " someone rolls 1 and loses. The winnings are split between everyone else." \
                    "\nNote: if there is a tie then I will do more rolls on my own to determine the winner."

SCRATCH_BUTTS = [':point_left:',
                 '<:weepinbell:425870197656780801>',
                 '<:bobface:455948634949943296>',
                 '<:dafuq:451983622140854277>',
                 ':melon:',
                 '<:zergling:231180053491351552>',
                 '<a:ditto:426978211046621185>',
                 '<:mareep:425868255522062337>',
                 '<a:spinkiss:452567956380057630>',
                 '<:mesowad:246852286993793025>',
                 ':middle_finger:',
                 ':hammer:',
                 '<:mesocoin:246852286914101248>',
                 ':cloud:',
                 ':cloud_tornado:',
                 '<a:nomnom:445818147845439504>',
                 ':thinking:',
                 ':wave:',
                 '<:bobface:455948634949943296>',
                 ':left_facing_fist:',
                 ':peach:',
                 ':100:',
                 ':revolving_hearts:',
                 ':hotsprings:',
                 ':notes:',
                 ':arrow_left:',
                 ':end:',
                 ':speech_balloon:',
                 ':anger_right:',
                 ':thought_balloon:',
                 ':loudspeaker:',
                 '<a:seizureditto:428052671891636224>',
                 ':fire:',
                 ':shower:',
                 ':tada:',
                 ':runner:',
                 ':cactus:',
                 '<:lurveyes:245292457741385728>',
                 ':eyes:',
                 ':pray:',
                 '<:psy:457036806089867264>',
                 ':eggplant:',
                 ':dash:',
                 ':whisky:',
                 '<:ban:384550483890536453>',
                 '<:f6:247983489603993600>',
                 '<a:talkatoo:440265764994547712>',
                 ':bow:',
                 ':kiss:',
                 ':unamused:',
                 ':selfie:',
                 '<:psyduckeyes:847363330658271232>'
                 ]


SPACE = ' '
DOUBLE_SPACE = '  '
CODE_TAG = '```'
LINEBREAK = '\n'

GAME_ID = {
    "SLOTS": 1,
    "RACE": 2,
    "SCRATCHCARD": 3,
    "HAMMERPOT": 4,
    "BLACKJACK": 5,
    "BOMBTILE": 6
}

TSUNDERE_BALL = [
    "I don't want to talk about it.",
    "Never mind.",
    "Forget about it.",
    "No.",
    "Sure.",
    "It's nothing. Don't worry about it.",
    "Well, maybe.",
    "Not particularly your business.",
    "Why do you care?",
    "Yes.",
    "(Annoyed sigh) No.",
    "Barely.",
    "Fine. Yes.",
    "Well, it's not like I don't agree...",
    "As long as it's me you're asking advice from, fine. (Yes.)",
    "As long as it's me you're asking advice from, fine. (No.)"
]