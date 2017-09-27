column_labels = ['`A`', '`B`', '`C`', '`D`', '`E`', '`F`', '`G`', '`H`', '`I`', '`J`']
column_inputs = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
corner = '.'
space = '    '
row_labels = ['`0`', '`1`', '`2`', '`3`', '`4`', '`5`', '`6`', '`7`', '`8`', '`9`']
row_inputs = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

neutral_tile = {'emote': ':white_medium_square:', 'value': 0}
empty_tile = {'emote': ':zero:', 'value': 0}
hundred = {'emote': ':100:', 'value': 100}
one = {'emote': ':one:', 'value': 1}
three = {'emote': ':three:', 'value': 3}
five = {'emote': ':five:', 'value': 5}
ten = {'emote': ':keycap_ten:', 'value': 10}


def start_message(author):
    return 'New scratch card for {}.'.format(author)


def attempt_message(attempts):
    return 'You have {} attempts remaining.'.format(attempts)


def num_matches_message(matches_to_win):
    return 'Match {} symbols to win!'.format(matches_to_win)