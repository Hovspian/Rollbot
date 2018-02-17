from typing import List


class Player:

    """
    Couples Discord member objects and their avatar within a game.
    """

    def __init__(self, user, avatar: any):
        self.user = user
        self.name = user.display_name
        self.avatar = avatar
        self.afk = 0
        self.gold_won = 0


class BlackjackPlayer(Player):

    """
    Methods for clarity.
    """

    def get_first_hand(self) -> any:
        return self.avatar[0]

    def get_hands(self) -> List[any]:
        return self.avatar
