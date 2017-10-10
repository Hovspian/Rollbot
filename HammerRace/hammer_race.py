from HammerRace.race_track import RaceTrack
from HammerRace.participant import Participant


class HammerRace:
    # Manage relationship between feedback, participants and race

    def __init__(self):
        self.distance_to_finish = 40
        self.winners = []
        self.participants = []
        self.race_track = RaceTrack(self)
        self.in_progress = False

    def next_round(self) -> None:
        [self._participant_turn(participant) for participant in self.participants]
        self._check_race_end()

    def valid_num_participants(self) -> bool:
        is_min_participants = len(self.participants) > 1
        is_max_participants = len(self.participants) <= 5
        return is_min_participants and is_max_participants

    def round_report(self) -> str:
        return self.race_track.draw_track()

    def winner_report(self) -> str:
        winners = self._get_winner_names()
        report = "The winners are {}" if self._has_multiple_winners() else "The winner is {}"
        return report.format(winners)

    def get_start_message(self):
        return None

    def is_winner(self, participant: Participant) -> bool:
        return self._get_steps_left(participant.progress) <= 0

    def _init_participant(self, short_name: str, name: str):
        participant = Participant(short_name, name)
        self._add_participant(participant)
        return participant

    def _participant_turn(self, participant: Participant) -> None:
        participant.make_move()
        if self.is_winner(participant):
            self._add_winner(participant)

    def _check_race_end(self) -> None:
        if self.is_race_end():
            self.in_progress = False

    def _get_steps_left(self, progress: int) -> int:
        character_space = 1
        return self.distance_to_finish - progress - character_space

    def _add_participant(self, participant: Participant) -> None:
        self.participants.append(participant)

    def _add_winner(self, participant: Participant) -> None:
        self.winners.append(participant)

    def is_race_end(self) -> bool:
        return len(self.winners) > 0

    def _has_multiple_winners(self) -> bool:
        return len(self.winners) > 1

    def _get_player_names(self) -> str:
        return ', '.join(player.name for player in self.participants)

    def _get_winner_names(self) -> str:
        return ', '.join(winner.name for winner in self.winners)