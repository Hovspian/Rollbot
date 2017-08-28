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
        self.y = self.init_participant(short_name='y', name='Yes')
        self.n = self.init_participant(short_name='n', name='No')
        self.h = self.init_participant(short_name='h', name=':hammer:')
        self.announcement.overriding_winner = self.h

        self.race.set_num_participants()

    def init_participant(self, short_name, name):
        participant = Participant(short_name, name)
        self.race.participants.append(participant)
        return participant

    def next_round(self):
        for participant in self.race.participants:
            participant.make_move()
            if self.race.check_winner(participant.progress):
                self.race.winners.append(participant)
        if len(self.race.winners) > 0:
            self.race_in_progress = False

    def round_report(self):
        return self.announcement.round_report()

    def winner_report(self):
        return self.announcement.winner() + '\n' + self.announcement.gold_owed()