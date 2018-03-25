class BombtilePlayer:
    def __init__(self, user):
        self.user = user
        self.name = user.display_name
        self.wager = 10
        self.multiplier = 1
        self.is_ai = False
        self.afk = False

    def set_afk(self, is_afk: bool) -> None:
        self.afk = is_afk

    def get_wager(self) -> int:
        return self.wager

    def get_multiplier(self) -> int:
        return self.multiplier

    def update_multiplier(self, multiplier: int) -> None:
        self.multiplier *= multiplier

    @staticmethod
    def create_ai(user) -> 'BombtilePlayer':
        ai = BombtilePlayer(user)
        ai.is_ai = True
        return ai
