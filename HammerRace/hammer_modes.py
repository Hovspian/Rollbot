from typing import List
from Core.constants import *
from HammerRace.hammer_race import *


class ClassicHammer(HammerRace):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.overriding_answer = None  # TBD
        self.init_players()

    def init_players(self) -> None:
        super()._init_player(short_name="y", name="yes")
        super()._init_player(short_name="n", name="no")
        hammer = super()._init_player(short_name="h", name=":hammer:")
        self.overriding_answer = hammer.name

    def outcome_report(self) -> str:
        answer = self._get_answer()
        report = SPACE.join(["The answer is", answer])
        if self.message != '':
            report = LINEBREAK.join([self.message, report])
        return report

    def _get_answer(self) -> str:
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
        self.invalid_players_error = "Please enter 2-5 options, separated by commas. " \
                                          "Example: ```/compare bread, eggs, hammer```"
        self._init_players()

    def outcome_report(self) -> str:
        return SPACE.join(["Out of",
                           self.message,
                           ":\n",
                           super().outcome_report()])

    def _init_players(self) -> None:
        [self._init_option(option) for option in self._options]

    def _init_option(self, option: str) -> None:
        option = option.strip()
        first_letter = option[0]
        super()._init_player(short_name=first_letter, name=option)

    @staticmethod
    def _set_options(message: str) -> List[str]:
        return message.split(",")


class VersusHammer(HammerRace):
    """Game mode allows users to join the race."""

    def __init__(self, ctx):
        HammerRace.__init__(self, ctx)
        self.losers = []
        self.multiplier = 1
        self.invalid_players_error = "A race needs at least two players."

    def get_start_message(self) -> str:
        return SPACE.join(["Race between", self._get_player_names()])

    def outcome_report(self) -> str:
        if not self.losers:
            return "Tie!"
        else:
            return LINEBREAK.join([super().outcome_report(), self._report_gold_owed()])

    def get_avatar(self, player):
        short_name = player.display_name[0]
        name = player.display_name
        return super()._init_player(short_name, name)

    def _report_gold_owed(self) -> str:
        reports = [self._get_gold_owed(loser) for loser in self.losers]
        return LINEBREAK.join(reports)

    def _check_race_end(self) -> None:
        if self.is_race_end():
            self.end_game()
            self._resolve_losers()

    def _resolve_losers(self) -> None:
        for player in self.players:
            if player not in self.winners:
                gold_owed = self._calculate_gold_owed(player)
                self._add_loser(player, gold_owed)

    def _calculate_gold_owed(self, player: Participant) -> int:
        steps_left = self._get_steps_left(player.progress)
        return steps_left * self.multiplier + 5

    def _add_loser(self, player, gold) -> None:
        num_winners = len(self.winners)
        debtor = {'name': player.name,
                  'gold': gold,
                  'divided_gold': gold // num_winners}
        self.losers.append(debtor)

    @staticmethod
    def _get_gold_owed(loser: dict) -> str:
        user = loser['name']
        amount = loser['divided_gold']
        return f'{user} owes {amount} gold to each winner.'
