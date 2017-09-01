from HammerRace.hammermanager import HammerRaceManager


class ClassicHammer(HammerRaceManager):
    # TODO might have its own announcer?

    def __init__(self):
        super().__init__()
        self.init_participants()

    def init_participants(self):
        super().init_participant(short_name='y', name='Yes')
        super().init_participant(short_name='n', name='No')
        hammer = super().init_participant(short_name='h', name=':hammer:')
        self.announcement.overriding_answer = hammer
        super().init_participants()

    def next_round(self):
        super().next_round()

    def check_race_end(self):
        super().check_race_end()

    def round_report(self):
        return super().round_report()

    def winner_report(self):
        return self.announcement.answer() + '\n' + super().winner_report()

class ComparisonHammer(HammerRaceManager):
    """Game mode compares different choices
    eg. /hammer eggs, bread, banana
    TODO: If a short name is duplicate it will look at proceeding letters in the long name.
    If none are available it will choose another available letter.
    Accepts up to 5. """

    def __init__(self, message):
        super().__init__()
        self.options = []
        self.set_options(message)
        self.init_participants()
        self.short_names = []

    def set_options(self, message):
        options = message.split(',')
        self.options = options

    def unique_short_name(self):
        # TODO select unique short_names for everything that comes through
        return True

    def init_participants(self):
        for option in self.options:
            option = option.strip()
            short_name = option[0].lower()
            name = option
            super().init_participant(short_name, name)
        super().init_participants()

    def next_round(self):
        super().next_round()

    def check_race_end(self):
        super().check_race_end()

    def round_report(self):
        return super().round_report()

    def winner_report(self):
        return self.announcement.winners()


class VersusHammer(HammerRaceManager):
    """TODO gamemode allows users to join in the race.
    eg. /hammerrace
    """