class PlayerAvatar:
    """ Couples Discord member objects and their avatar within a game """
    def __init__(self, user, avatar: any):
        self.user = user
        self.avatar = avatar