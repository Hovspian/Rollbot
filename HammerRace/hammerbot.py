from HammerRace.race import Race
from HammerRace.participant import Participant


class HammerRaceManager:
    """Manage relationship between participants and race"""

    def __init__(self):
        self.race = Race()
        self.race_in_progress = False

    def init_race(self):
        self.init_participants()
        self.race_in_progress = True

    def init_participants(self):
        self.y = self.init_participant(short_name='y', name='Yes')
        self.n = self.init_participant(short_name='n', name='No')
        self.h = self.init_participant(short_name='h', name=':hammer:')

        self.race.set_num_participants()

    def init_participant(self, short_name, name):
        participant = Participant(short_name=short_name, name=name)
        self.race.participants.append(participant)
        return participant

    def next_round(self):
        for participant in self.race.participants:
            participant.make_move()
            if self.race.check_winner(participant.progress):
                self.race.winners.append(participant)
        if len(self.race.winners) > 0:
            self.race_in_progress = False

    def report_round(self):
        """String representing the entire round"""
        participant_slots = []

        for participant in self.race.participants:
            if participant in self.race.winners:
                display_winner = self.string_winner_path(participant)
                participant_slots.append(display_winner)
            else:
                display_in_progress = self.string_progress_path(participant)
                participant_slots.append(display_in_progress)

        race_track = self.race.get_race_track()
        report = race_track.format(*participant_slots)
        return report

    def string_winner_path(self, participant: Participant):
        path = '|'
        for i in range(0, self.race.distance_to_finish):
            path += ' '
        path += '| {} |'.format(participant.short_name)
        return path

    def string_progress_path(self, participant: Participant):
        path = '|'
        for i in range(0, participant.progress):
            path += '~'
        path += participant.short_name

        steps_left = self.race.steps_left(participant.progress)
        for j in range(0, steps_left):
            path += ' '
        path += "|   |"
        return path

    def announce_winner(self):
        if self.h in self.race.winners:
            return 'The answer is {}'.format(self.h.name)
        elif len(self.race.winners) > 1:
            return 'The answer is maybe'

        winner_name = self.race.winners[0].name
        return 'The answer is {}'.format(winner_name)

    def announce_gold_owed(self):
        message = ''
        for participant in self.race.participants:
            if participant not in self.race.winners:
                steps_remaining = self.race.steps_left(participant.progress)
                gold = self.calculate_gold(steps_remaining)
                message += '{} owes {} gold.\n'.format(participant.short_name, gold)

        return message

    def calculate_gold(self, steps_remaining):
        return pow(steps_remaining, 2) * 3 + 100


class Announcer:
    """ TODO hold all methods related to representing the racetrack and announcing progress"""
