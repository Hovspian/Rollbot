from HammerRace.race_track import RaceTrack
from HammerRace.participant import Participant


class HammerRace:
    # Manage relationship between feedback, participants and race

    def __init__(self):
        self.distance_to_finish = 40
        self.winners = []
        self.losers = []
        self.players = []
        self.race_track = RaceTrack(self)
        self.in_progress = False

    def _init_participant(self, short_name: str, name: str):
        participant = Participant(short_name, name)
        self.add_participant(participant)
        return participant

    def next_round(self) -> None:
        [self._participant_turn(participant) for participant in self.players]
        self._check_race_end()

    def _participant_turn(self, participant: Participant) -> None:
        participant.make_move()
        if self.is_winner(participant):
            self.add_winner(participant)

    def valid_num_participants(self) -> bool:
        return (len(self.players) > 1) and (len(self.players) <= 5)

    def _check_race_end(self) -> None:
        if self.is_race_end():
            self.in_progress = False
            self.add_losers()

    def round_report(self) -> str:
        return self.get_full_track()

    def winner_report(self) -> str:
        winners = self.get_winner_name_list()
        report = "The winners are {}" if self.has_multiple_winners() else "The winner is {}"
        return report.format(winners)

    def get_full_track(self) -> str:
        return self.race_track.draw_track()

    def get_steps_left(self, progress: int) -> int:
        character_space = 1
        return self.distance_to_finish - progress - character_space

    def is_winner(self, participant: Participant) -> bool:
        if self.get_steps_left(participant.progress) <= 0:
            return True

    def add_participant(self, participant: Participant) -> None:
        self.players.append(participant)

    def add_winner(self, participant: Participant) -> None:
        self.winners.append(participant)

    def add_losers(self):
        for participant in self.players:
            if participant not in self.winners:
                self.losers.append(participant)

    def is_race_end(self) -> bool:
        return len(self.winners) > 0

    def has_multiple_winners(self) -> bool:
        return len(self.winners) > 1

    def get_winner_name_list(self) -> str:
        return ', '.join(winner.name for winner in self.winners)