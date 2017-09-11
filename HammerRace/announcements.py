from HammerRace.participant import Participant


class Announcement:
    # Return string announcements

    def __init__(self, race):
        self.race = race
        self.overriding_answer = ''

    def set_overriding_answer(self, answer):
        self.overriding_answer = answer

    def round_report(self):
        race_track = self.race.get_race_track()
        participant_slots = self.participant_slots()
        return race_track.format(*participant_slots)

    def participant_slots(self):
        slots = []
        for participant in self.race.participants:
            if self.race.is_winner(participant):
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

    def answer(self):
        answers = self.get_winner_name_list()
        if self.overriding_answer in answers:
            answer = '{}'.format(self.overriding_answer)
        elif len(answers) > 1:
            answer = 'maybe'
        else:
            answer = '{}'.format(answers[0])
        return 'The answer is ' + answer

    def gold_owed(self, participant: Participant):
        gold = self.race.calculate_gold_owed(participant.progress)
        return '{} owes {} gold.\n'.format(participant.short_name, gold)

    def winners(self):
        winners = self.get_winner_name_list()
        if len(winners) > 1:
            return "The winners are {}".format(winners)
        else:
            return "The winner is {}".format(winners[0])

    def get_winner_name_list(self):
        winner_names = (winner.name for winner in self.race.winners)
        return ', '.join(winner_names)
