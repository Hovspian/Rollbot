import random
import math
from typing import List
from GridGames.Slots.symbols import *
from GridGames.Slots.bias_mechanic import SlotsBias
from GridGames.Slots.slot_machine import SlotMachine


class BigSlots(SlotMachine):
    def __init__(self):
        super().__init__()
        self.num_columns = 5
        self.payout_multiplier = 1.5
        self.init_reel_size = self.num_columns * 2
        self.bias_mechanic = BigBias(self)

    def _roll_num_included_symbols(self):
        return random.randint(1, self.num_columns)


class BigBias(SlotsBias):
    def __init__(self, slot_machine):
        super().__init__(slot_machine)

    def _get_bias_options(self) -> List[int]:
        first_row = 0
        last_row = self.num_columns - 1
        random_index = random.randint(first_row, last_row)
        no_bias = -1
        return [random_index, random_index, random_index, first_row, last_row, no_bias, no_bias]


class GiantSlots(SlotMachine):
    def __init__(self):
        super().__init__()
        self.num_columns = 7
        self.payout_multiplier = 2
        self.bias_mechanic = GiantBias(self)

    def _roll_num_included_symbols(self):
        return random.randint(0, self.num_columns - 1)


class GiantBias(SlotsBias):
    def __init__(self, slot_machine):
        super().__init__(slot_machine)

    def _get_bias_options(self) -> List[int]:
        first_row = 0
        last_row = self.num_columns - 1
        random_index = random.randint(first_row, last_row)
        no_bias = -1
        return [random_index, random_index,
                first_row,
                last_row,
                no_bias, no_bias]


class ClassicSlots(SlotMachine):
    def __init__(self):
        super().__init__()
        self.default_outcomes = [CHERRY, CHERRY,
                                 STRAWBERRY, STRAWBERRY,
                                 PEAR, PEAR,
                                 PINEAPPLE,
                                 GRAPES,
                                 BUTT,
                                 MEAT,
                                 LEMON,
                                 BAR, BAR,
                                 HAMMER,
                                 CAKE,
                                 SEVEN]

    @staticmethod
    def get_win_message(matches, winning_stats, payout) -> str:
        linebreak = '\n'
        return linebreak.join([f'Rolled {matches}!',
                               f'{winning_stats}',
                               f':dollar: Payout is {payout} gold. :dollar:'])


class BigClassicSlots(BigSlots, ClassicSlots):
    def __init__(self):
        super().__init__()


class GiantClassicSlots(GiantSlots, ClassicSlots):
    def __init__(self):
        super().__init__()


class MapleSlots(SlotMachine):
    def __init__(self):
        super().__init__()
        self.default_outcomes = [BUBBLING, BUBBLING,
                                 WARBOW, WARBOW,
                                 MUSHROOM, MUSHROOM,
                                 SLIME, SLIME,
                                 KUMBI, KUMBI,
                                 PINKY,
                                 OCTOPUS,
                                 PEPE,
                                 MESOCOIN,
                                 STEELY,
                                 MESOBAG,
                                 PANLID]

    @staticmethod
    def get_win_message(matches, winning_stats, payout) -> str:
        linebreak = '\n'
        mesowad = '<:mesowad:246852286993793025>'
        return linebreak.join([f'Rolled {matches}!',
                               f'{winning_stats}',
                               f'{mesowad} Payout is {payout} mesos. {mesowad}'])


class BigMapleSlots(BigSlots, MapleSlots):
    def __init__(self):
        super().__init__()


class GiantMapleSlots(GiantSlots, MapleSlots):
    def __init__(self):
        super().__init__()
