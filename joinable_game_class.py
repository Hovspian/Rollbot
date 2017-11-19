from player_avatar import PlayerAvatar


class JoinableGame:
    def __init__(self, ctx):
        self.ctx = ctx
        self.host = ctx.message.author
        self.host_name = self.host.display_name
        self.users = []  # All users who join a game
        self.players = []  # List[PlayerAvatar]
        self.in_progress = False
        self.max_time_left = 180
        self.add_user(self.host)

    def add_user(self, user) -> None:
        self.users.append(user)
        avatar = self.get_avatar(user)
        self.add_player(user, avatar)

    def add_player(self, user, avatar) -> None:
        # Couples the avatar and user in a PlayerAvatar class and submits it to self.players
        player_avatar = PlayerAvatar(user, avatar)
        self.players.append(player_avatar)

    def get_avatar(self, user) -> any:
        # Method that constructs the user's in-game representation
        pass

    def get_context(self) -> object:
        # Info such as who started the game, what channel
        return self.ctx

    def get_host(self):
        return self.host

    def get_host_name(self):
        return self.host_name
