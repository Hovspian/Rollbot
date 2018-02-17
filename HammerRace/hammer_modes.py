from typing import List

from Core.constants import *
from Core.player_avatar import Player
from HammerRace.hammer_race import *


class ClassicHammer(HammerRace):
    def __init__(self, bot, ctx):
        super().__init__(bot, ctx)
        self.overriding_answer = None  # TBD
        self._init_players()

    def _init_players(self) -> None:
        super()._init_participant(short_name="y", name="yes")
        super()._init_participant(short_name="n", name="no")
        hammer = super()._init_participant(short_name="h", name=":hammer:")
        self.overriding_answer = hammer.name

    def _get_outcome_report(self) -> str:
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
    """
    Game mode compares inputted choices.
    Example: /hammer eggs, bread, banana
    """

    def __init__(self, bot, ctx):
        super().__init__(bot, ctx)
        self._options = self._set_options(self.message)
        self.invalid_players_error = "Please enter 2-5 options, separated by commas. " \
                                     "Example: ```/compare bread, eggs, hammer```"
        self._init_players()

    async def run(self):
        if self.valid_num_players():
            await super().run()
        else:
            await self.bot.say(self.invalid_players_error)

    def _get_outcome_report(self) -> str:
        return LINEBREAK.join([f"Out of {self.message}:",
                               self._get_winner_report()])

    def _init_players(self) -> None:
        for option in self._options:
            if option:
                self._init_option(option)

    def _init_option(self, option: str) -> None:
        option = option.strip()
        first_letter = option[0]
        super()._init_participant(short_name=first_letter, name=option)

    @staticmethod
    def _set_options(message: str) -> List[str]:
        return message.split(",")


class VersusHammer(HammerRace):
    """
    Game mode allows users to join the race.
    """

    def __init__(self, bot, ctx):
        super().__init__(bot, ctx)
        self.winning_players = []  # List[Player], used in resolving gold payouts.
        # Contrast with parent property "self.winners = List[Participant]." Other modes don't use the Player class.
        self.losers = []  # List[Player]
        self.invalid_players_error = "A race needs at least two players."
        self.payouts = []  # List[dict] data saved at the end of the game.

    async def run(self):
        if self.valid_num_players():  # TODO full at 5 people
            starting_message = SPACE.join(["Race between", self._get_participant_names()])
            await self.bot.say(starting_message)
            await super().run()
        else:
            await self.bot.say(self.invalid_players_error)

    def _get_outcome_report(self) -> str:
        if not self.winning_players:
            return "Tie!"
        else:
            return LINEBREAK.join([self._get_winner_report(), self._report_gold_owed()])

    def add_user(self, user):
        super().add_user(user)
        self.add_player(user)

    def add_player(self, user):
        avatar = self.get_avatar(user)
        player_avatar = Player(user, avatar)
        super().add_player(player_avatar)

    def get_avatar(self, user):
        short_name = user.display_name[0]
        name = user.display_name
        return self._init_participant(short_name, name)

    def _report_gold_owed(self) -> str:
        reports = [self.__get_gold_owed_report(loser) for loser in self.losers]
        return LINEBREAK.join(reports)

    def _check_race_end(self) -> None:
        if self.is_race_end():
            self.end_game()
            self._resolve_payouts()

    def _resolve_payouts(self) -> None:
        for player in self.players:
            self.__sort_winner_or_loser(player)
        for loser in self.losers:
            self.__dispense_payouts(loser)

    def __sort_winner_or_loser(self, player):
        participant = player.avatar
        if participant not in self.winners:
            self.__add_losing_player(player)
        else:
            self.__add_winning_player(player)

    def __dispense_payouts(self, loser: Player):
        gold_owed = self.__calculate_gold_owed(participant=loser.avatar)
        loser.gold_won -= gold_owed
        for winner in self.winning_players:
            winner.gold_won += gold_owed
            self.__add_payout(winner.user, gold_owed, loser.user)

    def __add_payout(self, to_user, amount, from_user):
        self.payouts.append({
            'to_user': to_user,
            'amount': amount,
            'from_user': from_user
        })

    def __calculate_gold_owed(self, participant: Participant) -> int:
        num_winners = len(self.winners)
        steps_left = self.get_steps_left(participant.progress)
        return (steps_left + 5) // num_winners

    def __add_losing_player(self, player) -> None:
        self.losers.append(player)

    def __add_winning_player(self, player) -> None:
        self.winning_players.append(player)

    @staticmethod
    def __get_gold_owed_report(loser: Player) -> str:
        amount = -loser.gold_won  # Reverse the negative int
        return f'{loser.name} owes {amount} gold to each winner.'
