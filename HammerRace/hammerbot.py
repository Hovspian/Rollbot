from HammerRace.race import Race
from HammerRace.participant import Participant
from HammerRace.announcements import Announcement


class HammerRaceManager:
    """Manage relationship between participants and race"""

    def __init__(self):
        self.race = Race()
        self.announcement = Announcement(self.race)
        self.race_in_progress = False

    def init_race(self):
        self.init_participants()
        self.race_in_progress = True

    def init_participants(self):
        self.init_participant(short_name='y', name='Yes')
        self.init_participant(short_name='n', name='No')
        hammer = self.init_participant(short_name='h', name=':hammer:')
        self.announcement.overriding_answer = hammer

        self.race.set_num_participants()

    def init_participant(self, short_name, name):
        participant = Participant(short_name, name)
        self.race.add_participant(participant)
        return participant

    def next_round(self):
        for participant in self.race.participants:
            participant.make_move()
            if self.race.check_winner(participant.progress):
                self.race.add_winner(participant)
        self.check_race_end()

    def check_race_end(self):
        if len(self.race.winners) > 0:
            self.race_in_progress = False

    def round_report(self):
        return self.announcement.round_report()

    def winner_report(self):
        return self.announcement.answer() + '\n' + self.announcement.gold_owed()