class Race:
    # Model of the race

    def __init__(self):
        self.distance_to_finish = 40
        self.winners = []
        self.losers = []
        self.participants = []

    def get_race_track(self):
        # String racetrack with placeholder participant slots
        linebreak = '\n'
        code_tag = '```'
        track_border = '+' + ('=' * self.get_border_size()) + '+' + linebreak

        race_track = code_tag + linebreak
        race_track += track_border
        race_track += self.get_participant_lanes()
        race_track += track_border
        race_track += code_tag

        return race_track

    def get_border_size(self):
        finish_line = 4
        return self.distance_to_finish + finish_line

    def get_participant_lanes(self):
        linebreak = '\n'
        last = -1
        empty_lane = '|' + (' ' * self.distance_to_finish) + '|   |' + linebreak
        participant_placeholder = '{}' + linebreak
        player_lanes = ''

        for participant in self.participants:
            player_lanes += participant_placeholder
            if participant != self.participants[last]:
                player_lanes += empty_lane

        return player_lanes

    def get_steps_left(self, participant_progress):
        character_space = 1
        steps_left = self.distance_to_finish - participant_progress - character_space
        return steps_left

    def is_winner(self, participant_progress):
        if self.get_steps_left(participant_progress) <= 0:
            return True

    def add_participant(self, participant):
        self.participants.append(participant)

    def add_winner(self, participant):
        self.winners.append(participant)

    def is_race_end(self):
        if len(self.winners) > 0:
            return True

    def has_multiple_winners(self):
        return len(self.winners) > 1

    def determine_losers(self):
        for participant in self.participants:
            if participant not in self.winners:
                self.losers.append(participant)

    def calculate_gold_owed(self, participant_progress):
        steps_left = self.get_steps_left(participant_progress)
        return pow(steps_left, 2) * 3 + 100
