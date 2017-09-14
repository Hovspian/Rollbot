from HammerRace.participant import Participant
from HammerRace.race import Race


class Announcement:
    # Return string announcements

    def __init__(self, race: Race):
        self.race = race

    def round_report(self):
        race_track = self.race.get_race_track()
        participant_slots = self.participant_slots()
        return race_track.format(*participant_slots)

    def participant_slots(self):
        slots = []
        for participant in self.race.participants:
            if self.race.is_winner(participant.progress):
                winning_participant = self.string_winner_path(participant)
                slots.append(winning_participant)
            else:
                participant_in_progress = self.string_progress_path(participant)
                slots.append(participant_in_progress)
        return slots

    def string_winner_path(self, participant: Participant):
        path = '|'
        path += ' ' * self.race.distance_to_finish
        path += '| {} |'.format(participant.short_name)
        return path

    def string_progress_path(self, participant: Participant):
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