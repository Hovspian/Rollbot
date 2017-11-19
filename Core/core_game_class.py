from Core.player_avatar import PlayerAvatar


class GameCore:
    def __init__(self, ctx):
        self.ctx = ctx
        self.host = ctx.message.author
        self.host_name = self.host.display_name
        self.users = []  # All users joining a game
        self.players = []  # Game participants
        self.in_progress = False
        self.add_user(self.host)

    def add_user(self, user) -> None:
        self.users.append(user)

    def add_player(self, player) -> None:
        self.players.append(player)

    def get_context(self) -> object:
        # Info such as who started the game, what channel
        return self.ctx

    def get_host(self):
        return self.host

    def get_host_name(self):
        return self.host_name

    def end_game(self):
        self.in_progress = False


class JoinableGame(GameCore):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.max_time_left = 180

    def add_player(self, user) -> None:
        # Couples the avatar and user in a PlayerAvatar class and submits it to self.players
        avatar = self.get_avatar(user)
        player_avatar = PlayerAvatar(user, avatar)
        super().add_player(player_avatar)

    def get_avatar(self, user) -> any:
        # Abstract method that constructs the user's in-game representation
        pass
