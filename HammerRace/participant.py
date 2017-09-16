import random


class Participant:
    def __init__(self, short_name: str, name: str):
        self._progress = 0
        self._min_move = 3
        self._max_move = 13
        self.short_name = short_name
        self.name = name

    def make_move(self, bonus=0) -> None:
        min_move = self._min_move + bonus
        roll = random.randint(min_move, self._max_move)
        self.progress += roll

    def get_progress(self):
        return self._progress

    def set_progress(self, amount: int):
        self._progress = amount

    progress = property(get_progress, set_progress)