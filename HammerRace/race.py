class Race:
    """Model of the race"""

    def __init__(self):
        self.distance_to_finish = 40
        self.num_participants = 0
        self.winners = []
        self.participants = []

    def get_race_track(self):
        """String racetrack with placeholder participant slots"""

        code_tag = '```'
        track_borders = '+============================================+' + '\n'
        empty_lane = '|                                        |   |' + '\n'
        participant_placeholder = '{}' + '\n'
        last = self.num_participants - 1

        race_track = code_tag + '\n'
        race_track += track_borders

        for i in range(0, self.num_participants):
            race_track += participant_placeholder
            if i != last:
                race_track += empty_lane

        race_track += track_borders
        race_track += code_tag

        return race_track

    def set_num_participants(self):
        self.num_participants = len(self.participants)

    def steps_left(self, participant_progress):
        character_space = 1
        steps_left = self.distance_to_finish - participant_progress - character_space
        return steps_left

    def check_winner(self, participant_progress):
        if self.steps_left(participant_progress) <= 0:
            return True
