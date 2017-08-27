from HammerRace.race import Race
from HammerRace.participant import Participant


class HammerRaceManager:
    """Sets up participants, puts rules into play, and determines progress"""

    def __init__(self):
        self.y = None
        self.n = None
        self.h = None
        self.race = Race()
        self.participants = []
        self.winners = []
        self.race_in_progress = False

    def init_participant(self, nametag, title):
        participant = Participant()
        participant.set_nametag(nametag)
        participant.set_title(title)
        self.participants.append(participant)
        return participant

    def init_participants(self):
        self.y = self.init_participant('y', 'Yes')
        self.n = self.init_participant('n', 'No')
        self.h = self.init_participant('h', ':hammer:')

        self.race.set_num_participants(len(self.participants))

    def init_race(self):
        self.init_participants()
        self.race_in_progress = True
        display_participants = []
        race_track = self.race.get_race_track()

        for participant in self.participants:
            display_participants.append(self.progress_position(participant))

        return race_track.format(*display_participants)

    def report_round(self):
        """String representing the entire round"""
        display_participants = self.next_round()
        race_track = self.race.get_race_track()
        report = race_track.format(*display_participants)
        return report

    def win_position(self, participant: Participant):
        """String representing a winner"""
        path = '|'
        for i in range(0, self.race.distance_to_finish):
            path += ' '
        path += '| {} |'.format(participant.nametag)
        return path

    def progress_position(self, participant: Participant):
        """String representing a character still racing"""
        path = '|'
        for i in range(0, participant.progress):
            path += '~'
        path += participant.nametag
        for j in range(0, self.race.steps_left(participant.progress)):
            path += ' '
        path += "|   |"
        return path

    def next_round(self):

        display_participants = []

        for participant in self.participants:
            participant.make_move()
            if self.race.check_winner(participant.progress):
                display_participants.append(self.win_position(participant))
                self.winners.append(participant)
            else:
                display_participants.append(self.progress_position(participant))

        if len(self.winners) > 0:
            self.race_in_progress = False

        return display_participants

    def announce_winner(self):
        if self.h in self.winners:
            return 'The answer is :hammer:'
        elif len(self.winners) > 1:
            return 'The answer is maybe'
        else:
            winner_title = self.winners[0].title

        return 'The answer is {}'.format(winner_title)

    def announce_gold_owed(self):
        """TODO announce gold owed by losing participants"""


class Announcer:
    """ TODO hold all methods related to representing the racetrack and announcing progress"""
