from HammerRace.participant import Participant
from typing import List


class Race:
    # Model of the race

    def __init__(self):
        self.distance_to_finish = 40
        self.winners = []
        self.losers = []
        self.participants = []

    def get_race_track(self) -> str:
        # Racetrack with placeholder participant slots
        linebreak = '\n'
        code_tag = '```'
        track_border = self._draw_border() + linebreak
        race_track = code_tag + linebreak
        race_track += track_border
        race_track += self._placeholder_participant_lanes()
        race_track += track_border
        race_track += code_tag
        return race_track

    def get_participant_slots(self) -> List[str]:
        return [self._draw_position(participant) for participant in self.participants]

    def get_steps_left(self, participant_progress: int) -> int:
        character_space = 1
        return self.distance_to_finish - participant_progress - character_space

    def is_winner(self, participant: Participant) -> bool:
        if self.get_steps_left(participant.progress) <= 0:
            return True

    def add_participant(self, participant: Participant) -> None:
        self.participants.append(participant)

    def add_winner(self, participant: Participant) -> None:
        self.winners.append(participant)

    def is_race_end(self) -> bool:
        if len(self.winners) > 0:
            return True

    def has_multiple_winners(self) -> bool:
        return len(self.winners) > 1

    def get_winner_name_list(self) -> str:
        winner_names = (winner.name for winner in self.winners)  # type: List[str]
        return ', '.join(winner_names)

    def _draw_border(self) -> str:
        finish_line_size = 4
        border_size = self.distance_to_finish + finish_line_size
        return '+{}+'.format('=' * border_size)

    def _placeholder_participant_lanes(self) -> str:
        lanes = ''
        linebreak = '\n'
        placeholder = '{}' + linebreak
        empty_lane = '|{}|   |'.format(' ' * self.distance_to_finish) + linebreak
        last = -1
        for participant in self.participants:
            lanes += placeholder
            if participant != self.participants[last]:
                lanes += empty_lane
        return lanes

    def _draw_position(self, participant: Participant) -> str:
        if self.is_winner(participant):
            path = self._winner_path()
        else:
            path = self._progress_path(participant.progress)
        return path.format(participant.short_name)

    def _winner_path(self) -> str:
        return '|' + (' ' * self.distance_to_finish) + '| {} |'

    def _progress_path(self, participant_progress: int) -> str:
        progress = '~' * participant_progress
        steps_left = ' ' * self.get_steps_left(participant_progress)
        return '|' + progress + "{}" + steps_left + "|   |"
