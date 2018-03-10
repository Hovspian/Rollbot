class GameCore:
    def __init__(self, ctx):
        self.ctx = ctx
        self.host = ctx.message.author
        self.host_name = self.host.display_name
        self.users = []  # All Discord users joining a game
        self.players = []  # PlayerAvatar[] if applicable

        # Flag for game started/ended. Determines whether /join and /forcestart are possible.
        # Also determines whether the game instance stays in scope.
        self.in_progress = False

        self.max_time_left = 180
        self.add_user(self.host)
        self.id = None

    def is_max_num_players(self) -> bool:
        """
        Set a maximum number of players in your multiplayer game, if applicable.
        No override == no max player limit.
        """
        return False

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

    def start_game(self):
        self.in_progress = True

    def end_game(self):
        self.in_progress = False

