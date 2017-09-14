from HammerRace.announcement import Announcement
from HammerRace.race import Race
from HammerRace.participant import Participant


class ClassicAnnouncement(Announcement):

    def __init__(self, race: Race):
        super().__init__(race)
        self.overriding_answer = ''

    def set_overriding_answer(self, answer):
        self.overriding_answer = answer

    def answer(self):
        answers = super().get_winner_name_list()
        if self.overriding_answer in answers:
            answer = '{}'.format(self.overriding_answer)
        elif self.race.has_multiple_winners():
            answer = 'maybe'
        else:
            answer = '{}'.format(answers[0])
        return 'The answer is ' + answer

    def round_report(self):
        return super().round_report()


class WinnerAnnouncement(Announcement):

    def __init__(self, race):
        super().__init__(race)

    def gold_owed(self, participant: Participant):
        gold = self.race.calculate_gold_owed(participant.progress)
        return '{} owes {} gold.\n'.format(participant.short_name, gold)

    def winners(self):
        winners = super().get_winner_name_list()
        if self.race.has_multiple_winners():
            return "The winners are {}".format(winners)
        return "The winner is {}".format(winners)

    def round_report(self):
        return super().round_report()