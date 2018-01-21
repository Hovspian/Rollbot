from typing import List


class PlayerAvatar:

    """ Couples Discord member objects and their avatar within a game """
    def __init__(self, user, avatar: any):
        self.user = user
        self.name = user.display_name
        self.avatar = avatar
        self.afk = 0
        self.gold_difference = 0  # Set at the end of a game


class AvatarHandler:

    """ Interprets the PlayerAvatar structure """

    @staticmethod
    def create_avatar(user, avatar) -> PlayerAvatar:
        return PlayerAvatar(user, avatar)

    @staticmethod
    def get_avatar(player: PlayerAvatar) -> any:
        return player.avatar

    @staticmethod
    def get_name(player: PlayerAvatar) -> str:
        return player.name


class BlackjackAvatarHandler(AvatarHandler):

    """ Method names in Blackjack for clarity """

    @staticmethod
    def create_avatar(user, hand) -> PlayerAvatar:
        return PlayerAvatar(user, [hand])

    @staticmethod
    def get_first_hand(player: PlayerAvatar) -> any:
        return player.avatar[0]

    def get_hands(self, player: PlayerAvatar) -> List[any]:
        return self.get_avatar(player)
