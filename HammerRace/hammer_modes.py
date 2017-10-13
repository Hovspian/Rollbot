from HammerRace.hammer_race import *
from constants import *
from typing import List
from player_avatar import PlayerAvatar


class ClassicHammer(HammerRace):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.overriding_answer = ""
        self.init_participants()

    def init_participants(self) -> None:
        super()._init_participant(short_name="y", name="yes")
        super()._init_participant(short_name="n", name="no")
        hammer = super()._init_participant(short_name="h", name=":hammer:")
        self.overriding_answer = hammer.name

    def winner_report(self) -> str:
        answer = self._get_answer()
        report = SPACE.join(["The answer is", answer])
        if self.message != '':
            report = LINEBREAK.join([self.message, report])
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

    def __init__(self, ctx):
        super().__init__(ctx)
        self._options = self._set_options(self.message)
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
                           self.message,
                           ":\n",
                           super().winner_report()])


class VersusHammer(HammerRace):
    """Game mode allows users to join the race."""

    def __init__(self, ctx):
        super().__init__(ctx)
        self.host = ctx.message.author
        self.players = []
        self.losers = []
        self.add_user(self.host)
        self.setup_message = f"{self.host.display_name} has started a race."
        self.invalid_participants_error = "A race needs at least two players."

    def get_start_message(self):
        return SPACE.join(["Race between", self._get_player_names()])

    def add_user(self, user):
        short_name = user.display_name[0]
        name = user.display_name
        participant = super()._init_participant(short_name, name)
        player_avatar = PlayerAvatar(user, avatar=participant)
        self.players.append(player_avatar)

    def winner_report(self):
        if not self.losers:
            return "Tie!"
        else:
            return LINEBREAK.join([super().winner_report(), self.report_gold_owed()])

    def report_gold_owed(self):
        reports = [self.gold_owed(loser) for loser in self.losers]
        return LINEBREAK.join(reports)

    def gold_owed(self, participant: Participant):
        steps_left = self._get_steps_left(participant.progress)
        gold = steps_left * 2 + 5
        gold = gold // len(self.winners)
        return f'{participant.name} owes {gold} gold to each winner.'

    def _check_race_end(self) -> None:
        if self.is_race_end():
            self.in_progress = False
            self._add_losers()

    def _add_losers(self):
        for participant in self.participants:
            if participant not in self.winners:
                self.losers.append(participant)