from HammerRace.participant import Participant


class Announcement:

    def __init__(self, race):
        self.race = race
        self.overriding_answer = None

    def round_report(self):
        race_track = self.race.get_race_track()
        participant_slots = self.participant_slots()
        return race_track.format(*participant_slots)

    def participant_slots(self):
        slots = []
        for participant in self.race.participants:
            if participant in self.race.winners:
                winning_participant = self.string_winner_path(participant)
                slots.append(winning_participant)
            else:
                participant_in_progress = self.string_progress_path(participant)
                slots.append(participant_in_progress)
        return slots

    def string_winner_path(self, participant: Participant):
        path = '|'
        for i in range(0, self.race.distance_to_finish):
            path += ' '
        path += '| {} |'.format(participant.short_name)
        return path

    def string_progress_path(self, participant: Participant):
        progress = self.get_progress(participant.progress)
        steps_left = self.get_steps_left(participant.progress)
        path = '|' + progress + participant.short_name + steps_left + "|   |"
        return path

    def get_progress(self, progress):
        path_part = ''
        for i in range(0, progress):
            path_part += '~'
        return path_part

    def get_steps_left(self, progress):
        path_part = ''
        steps_left = self.race.steps_left(progress)
        for j in range(0, steps_left):
            path_part += ' '
        return path_part

    def answer(self):
        if self.overriding_answer in self.race.winners:
            return 'The answer is {}'.format(self.overriding_answer.name)
        elif len(self.race.winners) > 1:
            return 'The answer is maybe'
        winner_name = self.race.winners[0].name
        return 'The answer is {}'.format(winner_name)

    def gold_owed(self):
        """TODO divide by the number of winners"""
        message = ''
        for participant in self.race.participants:
            if participant not in self.race.winners:
                steps_remaining = self.race.steps_left(participant.progress)
                gold = self.calculate_gold(steps_remaining)
                message += '{} owes {} gold.\n'.format(participant.short_name, gold)
        return message

    def calculate_gold(self, steps_remaining):
        return pow(steps_remaining, 2) * 3 + 100

    def winners(self):
        if len(self.race.winners) > 1:
            winner_list = self.get_list_of_winners()
            return "The winners are {}".format(winner_list)
        else:
            return "The winner is {}".format(self.race.winners[0])

    def get_list_of_winners(self):
        winner_list = ''
        last = len(self.race.winners) - 1
        for winner in self.race.winners:
            winner_list += winner
            if winner != last:
                winner_list += ', '
        return winner_list
