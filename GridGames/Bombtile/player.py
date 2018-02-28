class BombtilePlayer:
    def __init__(self, user):
        self.user = user
        self.name = user.display_name
        self.wager = 10
        self.multiplier = 1
        self.afk = 0

    def get_wager(self):
        return self.wager

    def get_multiplier(self):
        return self.multiplier

    def update_multiplier(self, multiplier: int):
        self.multiplier *= multiplier
