import random
from typing import List


def filter_value(container, value_to_filter):
    return [value for value in container if value != value_to_filter]


def roll(input_list: List) -> any:
    pick = random.randint(0, len(input_list) - 1)
    return input_list[pick]


def loop_list_value(index, container) -> int:
    list_size = len(container)
    return index % list_size
