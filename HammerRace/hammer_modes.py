from HammerRace.hammer_manager import HammerRaceManager
from HammerRace.sub_announcements import *


class ClassicHammer(HammerRaceManager):

    def __init__(self):
        super().__init__(ClassicAnnouncement)
        self.init_participants()

    def init_participants(self):
        super().init_participant(short_name='y', name='Yes')
        super().init_participant(short_name='n', name='No')
        hammer = super().init_participant(short_name='h', name=':hammer:')
        self.announcement.set_overriding_answer(hammer.name)

    def next_round(self):
        super().next_round()

    def round_report(self):
        return super().round_report()

    def winner_report(self):
        return self.announcement.answer()


class ComparisonHammer(HammerRaceManager):
    """Game mode compares inputted choices.
    Example: /hammer eggs, bread, banana"""

    def __init__(self, message):
        super().__init__(WinnerAnnouncement)
        self.options = []
        self.set_options(message)
        self.init_participants()

    def set_options(self, message):
        self.options = message.split(',')

    def init_participants(self):
        for option in self.options:
            option = option.strip()
            super().init_participant(short_name=option[0], name=option)

    def valid_num_participants(self):
        if (len(self.race.participants) > 1) and (len(self.race.participants) <= 5):
            return True

    def next_round(self):
        super().next_round()

    def round_report(self):
        return super().round_report()

    def winner_report(self):
        return self.announcement.winners()


class VersusHammer(HammerRaceManager):
    """TODO gamemode allows users to join in the race.
    eg. /hammerrace
    """
    def __init__(self, game_starter):
        super().__init__(WinnerAnnouncement)
        self.users = []

    def sign_up(self, participant):
        self.add_user_participant(participant)
        short_name = participant[0]
        name = participant
        super().init_participant(short_name, name)
        print(name + "joined the game as + " + short_name)

    def add_user_participant(self, user):
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
