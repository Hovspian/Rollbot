from HammerRace.hammer_manager import *


class ClassicHammer(HammerRaceManager):

    def __init__(self):
        super().__init__()
        self.overriding_answer = ''
        self.init_participants()

    def init_participants(self) -> None:
        super()._init_participant(short_name='y', name='Yes')
        super()._init_participant(short_name='n', name='No')
        hammer = super()._init_participant(short_name='h', name=':hammer:')
        self.overriding_answer = hammer.name

    def winner_report(self) -> str:
        answer_list = self.race.get_winner_name_list()
        if self.overriding_answer in answer_list:
            answer = self.overriding_answer
        elif self.race.has_multiple_winners():
            answer = 'maybe'
        else:
            answer = answer_list
        return 'The answer is ' + answer


class ComparisonHammer(HammerRaceManager):
    """Game mode compares inputted choices.
    Example: /hammer eggs, bread, banana"""

    def __init__(self, message: str):
        super().__init__()
        self._options = []
        self._set_options(message)
        self._init_participants()

    def _set_options(self, message: str) -> None:
        self._options = message.split(',')

    def _init_participants(self) -> None:
        [self._init_option(option) for option in self._options]

    def _init_option(self, option: str) -> None:
        option = option.strip()
        first_letter = option[0]
        super()._init_participant(short_name=first_letter, name=option)

    def valid_num_participants(self) -> bool:
        if (len(self.race.participants) > 1) and (len(self.race.participants) <= 5):
            return True


class VersusHammer(HammerRaceManager):
    """TODO game mode allows users to join in the race.
    eg. /start race
    """
    def __init__(self, game_starter):
        super().__init__()
        self.users = []

    def sign_up(self, participant):
        self.add_user(participant)
        short_name = participant[0]
        name = participant
        super()._init_participant(short_name, name)
        print(name + "joined the game as + " + short_name)

    def add_user(self, user):
        self.users.append(user)

    def valid_participant(self, user):
        if user not in self.users:
            return True

    def valid_max_participants(self):
        if self.race.num_participants <= 5:
            return True

    def valid_min_participants(self):
        if self.race.num_participants > 1:
            return True

    def winner_report(self):
        return super().winner_report() + self.report_gold_owed()

    def report_gold_owed(self):
        linebreak = '\n'
        reports = [self.gold_owed(loser) for loser in self.race.losers]
        return linebreak.join(reports)

    def gold_owed(self, participant: Participant):
        steps_left = self.race.get_steps_left(participant.progress)
        gold = pow(steps_left, 2) * 3 + 100
        return '{} owes {} gold.'.format(participant.short_name, gold)
