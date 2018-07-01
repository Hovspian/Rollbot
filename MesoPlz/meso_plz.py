import random

from Core.core_game_class import GameCore
from Core.helper_functions import roll

LOWER_RANGE = ([(1, 10)] * 3 +
               [(11, 20)])

UPPER_RANGE = ([(21, 40)] * 5 +
               [(41, 99)] * 4 +
               [(100, 150)] * 3 +
               [(151, 250)] * 2 +
               [(251, 500)])


class MesoPlz(GameCore):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.payout = 0

    def run(self) -> None:
        bound_num = random.randint(0, 10)
        bound = self.__get_bound(bound_num)
        self.payout = random.randint(bound[0], bound[1])

    def get_payout(self) -> int:
        return self.payout

    @staticmethod
    def __get_bound(num: int) -> tuple:
        """
        :param num: An int from range 0-10.
        :return: tuple: An int range for given mesos.
        """
        if num == 0:
            return 0, 0
        elif 0 < num <= 9:
            return roll(LOWER_RANGE)
        else:
            return roll(UPPER_RANGE)
