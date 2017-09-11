class Race:
    # Model of the race

    def __init__(self):
        self.distance_to_finish = 40
        self.num_participants = 0
        self.winners = []
        self.participants = []

    def get_race_track(self):
        # String racetrack with placeholder participant slots

        code_tag = '```'
        linebreak = '\n'
        track_borders = '+============================================+' + linebreak
        empty_lane = '|                                        |   |' + linebreak
        participant_placeholder = '{}' + linebreak
        last = -1

        race_track = code_tag + linebreak
        race_track += track_borders

        for participant in self.participants:
            race_track += participant_placeholder
            if participant != self.participants[last]:
                race_track += empty_lane

        race_track += track_borders
        race_track += code_tag

        return race_track

    def get_steps_left(self, participant_progress):
        character_space = 1
        steps_left = self.distance_to_finish - participant_progress - character_space
        return steps_left

    def is_winner(self, participant):
        if self.get_steps_left(participant.progress) <= 0:
            return True

    def add_participant(self, participant):
        self.participants.append(participant)

    def add_winner(self, participant):
        self.winners.append(participant)

    def is_race_end(self):
        if len(self.winners) > 0:
            return True

    def calculate_gold_owed(self, participant_progress):
        steps_left = self.get_steps_left(participant_progress)
        return pow(steps_left, 2) * 3 + 100