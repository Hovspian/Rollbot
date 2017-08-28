import random


class Participant:
    def __init__(self):
        self.progress = 0
        self.min_move = 3
        self.max_move = 13
        self.nametag = ''
        self.title = ''

    def set_nametag(self, name):
        self.nametag = name

    def set_title(self, title):
        self.title = title

    def make_move(self, bonus=0):
        min_move = self.min_move + bonus
        roll = random.randint(min_move, self.max_move)
        self.progress += roll
