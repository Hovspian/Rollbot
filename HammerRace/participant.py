import random


class Participant:
    def __init__(self, short_name: str, name: str):
        self.progress = 0
        self.min_move = 3
        self.max_move = 13
        self.short_name = short_name
        self.name = name

    def make_move(self, bonus=0) -> None:
        min_move = self.min_move + bonus
        roll = random.randint(min_move, self.max_move)
        self.progress += roll
