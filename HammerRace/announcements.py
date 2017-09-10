from HammerRace.participant import Participant


class Announcement:

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
            if participant.name in self.race.winner_names:
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
        progress = self.get_progress_part(participant.progress)
        steps_left = self.get_steps_remaining_part(participant.progress)
        path = '|' + progress + participant.short_name + steps_left + "|   |"
        return path

    @staticmethod
    def get_progress_part(progress):
        path_part = '~' * progress
        return path_part

    def get_steps_remaining_part(self, progress):
        path_part = ' ' * self.race.steps_left(progress)
        return path_part

    def answer(self):
        if self.overriding_answer in self.race.winner_names:
            return 'The answer is {}'.format(self.overriding_answer)
        if len(self.race.winner_names) > 1:
            return 'The answer is maybe'
        winner_name = self.race.winner_names[0]
        return 'The answer is {}'.format(winner_name)

    def gold_owed(self):
        """TODO divide by the number of winners"""
        message = ''
        for participant in self.race.participants:
            if participant.name not in self.race.winner_names:
                steps_remaining = self.race.steps_left(participant.progress)
                gold = self.calculate_gold(steps_remaining)
                message += '{} owes {} gold.\n'.format(participant.short_name, gold)
        return message

    @staticmethod
    def calculate_gold(steps_remaining):
        """TODO move this method away"""
        return pow(steps_remaining, 2) * 3 + 100

    def winners(self):
        if len(self.race.winner_names) > 1:
            winner_list = self.get_list_of_winners()
            return "The winners are {}".format(winner_list)
        else:
            winner_name = self.race.winner_names[0]
            return "The winner is {}".format(winner_name)

    def get_list_of_winners(self):
        return ', '.join(self.race.winner_names)
