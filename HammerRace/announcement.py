from HammerRace.participant import Participant
from HammerRace.race import Race


class Announcement:
    # Return string announcements

    def __init__(self, race: Race):
        self.race = race

    def round_report(self):
        race_track = self.race.get_race_track()
        participant_slots = self.get_participant_slots()
        return race_track.format(*participant_slots)

    def get_participant_slots(self):
        return [self.draw_position(participant) for participant in self.race.participants]

    def draw_position(self, participant):
        if self.race.is_winner(participant.progress):
            return self.winner_path(participant)
        return self.progress_path(participant)

    def winner_path(self, participant: Participant):
        path = '|'
        path += ' ' * self.race.distance_to_finish
        path += '| {} |'.format(participant.short_name)
        return path

    def progress_path(self, participant: Participant):
        progress = '~' * participant.progress
        steps_left = ' ' * self.race.get_steps_left(participant.progress)
        path = '|' + progress + participant.short_name + steps_left + "|   |"
        return path

    def get_winner_name_list(self):
        winner_names = (winner.name for winner in self.race.winners)
        return ', '.join(winner_names)

    def get_loser_name_list(self):
        loser_names = (loser.name for loser in self.race.losers)
        return ', '.join(loser_names)