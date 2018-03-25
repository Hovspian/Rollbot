"""
A pool of all "AI players" who can join a game and make automatic plays on their turn.
They have varying names, but their user is always Rollbot (bot.user).
"""
from Core.helper_functions import roll

DIAS = '<:dias:427267672472944642> [AI] Dias'
LOGI = '<:logi:427267549059612673> [AI] Logi'
TOFU = '<:greenmatty:427289108050870272> [AI] Spicytofu'
ZERGY = '<:zergling:231180053491351552> [AI] Zergy'
TOKKO = '<:tokko:427290643933691905> [AI] Tokko'
BOWSER = '<:bowser:427291247460352012> [AI] Bowser'
KKR = '<:kkr:427291424304922624> [AI] King K. Rool'


class AiUser:
    """
    Mimic some fields of Discord user.
    """
    def __init__(self, character: str, bot_id: str):
        self.display_name = character
        self.id = bot_id


class AiUserGenerator:
    """
    Create a random unique AiUser.
    """

    def __init__(self, bot):
        self.bot_id = bot.user.id
        self.ai_characters = [
            DIAS,
            LOGI,
            TOFU,
            ZERGY,
            TOKKO,
            BOWSER,
            KKR
        ]

    def get_ai_user(self) -> AiUser:
        character = roll(self.ai_characters)
        self.ai_characters.remove(character)
        return self.__create(character)

    def __create(self, character) -> AiUser:
        return AiUser(character, self.bot_id)
