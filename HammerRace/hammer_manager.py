from HammerRace.race import Race
from HammerRace.participant import Participant


class HammerRaceManager:
    # Manage relationship between feedback, participants and race

    def __init__(self, announcement):
        self.race = Race()
        self.announcement = announcement(self.race)
        self.race_in_progress = True

    def init_participant(self, short_name, name):
        participant = Participant(short_name, name)
        self.race.add_participant(participant)
        return participant

    def next_round(self):
        for participant in self.race.participants:
            participant.make_move()
            if self.race.is_winner(participant.progress):
                self.race.add_winner(participant)
        self.check_race_end()

    def check_race_end(self):
        if self.race.is_race_end():
            self.race.determine_losers()
            self.race_in_progress = False

    def round_report(self):
        return self.announcement.round_report()
