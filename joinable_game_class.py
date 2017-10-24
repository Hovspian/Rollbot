from player_avatar import PlayerAvatar


class JoinableGame:
    def __init__(self, host):
        self.host = host
        self.host_name = host.display_name
        self.users = [host]  # All users who join a game
        self.players = []  # List[PlayerAvatar]
        self.in_progress = False
        self.max_time_left = 180

    def add_user(self, user):
        self.users.append(user)
        avatar = self.get_avatar(user)
        self.add_player(user, avatar)

    def add_player(self, user, avatar):
        # Couples the avatar and user in a PlayerAvatar class and submits it to self.players
        player_avatar = PlayerAvatar(user, avatar)
        self.players.append(player_avatar)

    def get_avatar(self, user) -> any:
        # Method that constructs the user's in-game representation
        pass
