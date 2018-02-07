class GameCore:
    def __init__(self, ctx):
        self.ctx = ctx
        self.host = ctx.message.author
        self.host_name = self.host.display_name
        self.users = []  # All Discord users joining a game
        self.players = []  # PlayerAvatar[] if applicable
        self.in_progress = False  # Flag for game started/ended. Determines whether /join and /forcestart are possible.
        self.max_time_left = 180
        self.add_user(self.host)
        self.title = "Game"
        self.payouts = []
        self.id = 0  # Unique int to identify game type. See GAME_ID in Core.constants.py

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

