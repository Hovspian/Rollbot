from typing import List


class PlayerAvatar:

    """ Couples Discord member objects and their avatar within a game """
    def __init__(self, user, avatar: any):
        self.user = user
        self.name = user.display_name
        self.avatar = avatar
        self.afk = 0
        self.gold_difference = 0  # Set at the end of a game


class BlackjackPlayer(PlayerAvatar):

    """ Method names for clarity """

    @staticmethod
    def create_avatar(user, hand) -> PlayerAvatar:
        return PlayerAvatar(user, [hand])

    def get_first_hand(self) -> any:
        return self.avatar[0]

    def get_hands(self) -> List[any]:
        return self.avatar
