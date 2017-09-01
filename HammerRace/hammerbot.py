from HammerRace.race import Race
from HammerRace.participant import Participant
from HammerRace.announcements import Announcement


class HammerRaceManager:
    """Manage relationship between participants and race"""

    def __init__(self):
        self.race = Race()
        self.announcement = Announcement(self.race)
        self.race_in_progress = True

    def init_participants(self):
        self.race.set_num_participants()

    def init_participant(self, short_name, name):
        participant = Participant(short_name, name)
        self.race.add_participant(participant)
        return participant

    def next_round(self):
        for participant in self.race.participants:
            participant.make_move()
            if self.race.check_winner(participant.progress):
                self.race.add_winner(participant)
        self.check_race_end()

    def check_race_end(self):
        if len(self.race.winners) > 0:
            self.race_in_progress = False

    def round_report(self):
        return self.announcement.round_report()

    def winner_report(self):
        return self.announcement.gold_owed()


class ClassicHammer(HammerRaceManager):
    """TODO might have its own announcer?"""

    def __init__(self):
        super().__init__()
        self.init_participants()

    def init_participants(self):
        super().init_participant(short_name='y', name='Yes')
        super().init_participant(short_name='n', name='No')
        hammer = super().init_participant(short_name='h', name=':hammer:')
        super().announcement.overriding_answer = hammer

        super().init_participants()

    def next_round(self):
        super().next_round()

    def check_race_end(self):
        super().check_race_end()

    def round_report(self):
        super().round_report()

    def winner_report(self):
        return super().announcement.answer() + '\n' + super().winner_report()

class ComparisonHammer(HammerRaceManager):
    """TODO gamemode compares different choices entered by users.
    eg. /hammer eggs, bread, banana
    If a short name is duplicate it will look at proceeding letters in the long name.
    If none are available it will choose another available letter.
    Accepts up to 5. """

    def __init__(self, message):
        super().__init__()
        self.options = []
        self.set_options(message)
        self.short_names = []

    def set_options(self, message):
        options = message.split(',')
        command_msg = 0
        options.pop(command_msg)
        """TODO remove spaces at the beginning/end of options"""
        self.options = options

    def unique_short_name(self):
        """TODO select unique short_names for everything that comes through"""
        return True

    def init_participants(self):
        for option in self.options:
            short_name = option[0][0]
            name = option[0]
            super().init_participant(short_name, name)

    def next_round(self):
        super().next_round()

    def check_race_end(self):
        super().check_race_end()

    def round_report(self):
        super().round_report()

    def winner_report(self):
        return super().announcement.winners()


class VersusHammer(HammerRaceManager):
    """TODO gamemode allows users to join in the race.
    eg. /hammerrace
    """