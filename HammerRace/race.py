class Race:

    """Model and constants of the race"""
    def __init__(self):
        self.round = 0
        self.distance_to_finish = 40
        self.num_participants = 0

    def get_race_track(self):
        """string racetrack with placeholder participant slots"""

        code_tag = '```'
        track_borders = '+============================================+' + '\n'
        empty_lane = '|                                        |   |' + '\n'
        player_placeholder = '{}' + '\n'
        last = self.num_participants - 1

        message = code_tag + '\n'
        message += track_borders

        for i in range(0, self.num_participants):
            message += player_placeholder
            if i != last:
                message += empty_lane

        message += track_borders
        message += code_tag

        return message

    def set_num_players(self, num):
        self.num_participants = num

    def increment_round(self):
        self.round += 1

    def steps_left(self, player_progress):
        character_space = 1
        steps_left = self.distance_to_finish - player_progress - character_space
        return steps_left

    def check_winner(self, player_progress):
        if self.steps_left(player_progress) <= 0:
            return True