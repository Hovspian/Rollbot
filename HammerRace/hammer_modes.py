from HammerRace.hammer_race import *
from constants import *
from typing import List


class ClassicHammer(HammerRace):
    def __init__(self, question):
        super().__init__()
        self.overriding_answer = ""
        self.question = question
        self.init_participants()

    def init_participants(self) -> None:
        super()._init_participant(short_name="y", name="yes")
        super()._init_participant(short_name="n", name="no")
        hammer = super()._init_participant(short_name="h", name=":hammer:")
        self.overriding_answer = hammer.name

    def winner_report(self) -> str:
        answer = self._get_answer()
        report = SPACE.join(["The answer is", answer])
        if self.question != '':
            report = LINEBREAK.join([self.question, report])
        return report

    def _get_answer(self):
        answer_list = self._get_winner_names()
        if self.overriding_answer in answer_list:
            answer = self.overriding_answer
        elif self._has_multiple_winners():
            answer = "maybe"
        else:
            answer = answer_list
        return answer


class ComparisonHammer(HammerRace):
    """Game mode compares inputted choices.
    Example: /hammer eggs, bread, banana"""

    def __init__(self, message: str):
        super().__init__()
        self._options_message = message
        self._options = self._set_options(message)
        self.invalid_participants_error = "Please enter 2-5 options, separated by commas. " \
                                          "Example: ```/compare bread, eggs, hammer```"
        self._init_participants()

    @staticmethod
    def _set_options(message: str) -> List[str]:
        return message.split(",")

    def _init_participants(self) -> None:
        [self._init_option(option) for option in self._options]

    def _init_option(self, option: str) -> None:
        option = option.strip()
        first_letter = option[0]
        super()._init_participant(short_name=first_letter, name=option)

    def winner_report(self):
        return SPACE.join(["Out of",
                           self._options_message,
                           ":\n",
                           super().winner_report()])


class VersusHammer(HammerRace):
    """Game mode allows users to join the race."""

    def __init__(self, game_starter):
        super().__init__()
        self.joining_message = "A race is starting."
        self.invalid_participants_error = "Not enough players."
        self.starting_message = SPACE.join(["Race between ", SPACE.join(self.players)])
        self.add_user(game_starter)

    def add_user(self, user):
        short_name = user.display_name[0]
        name = user.display_name
        super()._init_participant(short_name, name)

    def winner_report(self):
        return LINEBREAK.join([super().winner_report(), self.report_gold_owed()])

    def report_gold_owed(self):
        reports = [self.gold_owed(loser) for loser in self.losers]
        return LINEBREAK.join(reports)

    def gold_owed(self, participant: Participant):
        steps_left = self.get_steps_left(participant.progress)
        gold = steps_left * 2 + 5
        gold = gold // len(self.winners)
        return f'{participant.name} owes {gold} gold to each winner.'
