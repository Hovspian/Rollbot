from HammerRace.race import Race
from HammerRace.participant import Participant


class HammerRaceManager:

    """Concerned with setting up the players, putting rules into play, and determining progress"""
    def __init__(self):
        self.race = Race()
        self.players = []
        self.winners = []
        self.race_in_progress = False

    def init_char(self, nametag, title):
        player = Participant()
        player.set_nametag(nametag)
        player.set_title(title)
        self.players.append(player)
        return player

    def init_chars(self):
        self.y = self.init_char('y', 'Yes')
        self.n = self.init_char('n', 'No')
        self.h = self.init_char('h', ':hammer:')

        num = len(self.players)
        self.race.set_num_players(num)

    def init_race(self):
        self.init_chars()
        self.race_in_progress = True
        round_progress = []
        race_track = self.race.get_race_track()

        for player in self.players:
            round_progress.append(self.display_position(player))

        return race_track.format(*round_progress)

    def report_next_round(self):
        """report the state of the entire round"""
        round_progress = self.next_round()
        race_track = self.race.get_race_track()
        report = race_track.format(*round_progress)
        return report

    def display_win_position(self, player : Participant):
        path = '|'
        for i in range(0, self.race.distance_to_finish):
            path += ' '
        path += '| {} |'.format(player.nametag)
        return path

    def display_position(self, player : Participant):
        path = '|'
        for i in range(0, player.progress):
            path += '~'
        path += player.nametag
        for j in range(0, self.race.steps_left(player.progress)):
            path += ' '
        path += "|   |"
        return path

    def next_round(self):

        round_progress = []

        for player in self.players:
            player.make_move()
            if self.race.check_winner(player.progress):
                round_progress.append(self.display_win_position(player))
                self.winners.append(player)
            else:
                round_progress.append(self.display_position(player))

        if len(self.winners) > 0:
            self.race_in_progress = False

        self.race.increment_round()
        return round_progress

    def announce_winner(self):
        if self.h in self.winners:
            return 'The answer is :hammer:'
        elif len(self.winners) > 1:
            return 'The answer is maybe'
        else:
            winner_title = self.winners[0].title

        return 'The answer is {}'.format(winner_title)

    def announce_gold_owed(self):
        """TODO announce gold owed by losing participants"""


class Announcer:
    """ TODO hold all methods related to representing the racetrack and announcing progress"""
