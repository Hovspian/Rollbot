from HammerRace.participant import Participant
from typing import List


class Race:
    # Model of the race

    def __init__(self):
        self.distance_to_finish = 40
        self.winners = []
        self.losers = []
        self.participants = []
        self.race_track = RaceTrack(self)

    def get_full_track(self) -> str:
        race_track = self.race_track.draw_track()
        participant_slots = self.race_track.get_participant_slots()
        return race_track.format(*participant_slots)

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
        return len(self.winners) > 0

    def has_multiple_winners(self) -> bool:
        return len(self.winners) > 1

    def get_winner_name_list(self) -> str:
        return ', '.join(winner.name for winner in self.winners)


class RaceTrack:
    # Draw race track and participant strings
    def __init__(self, race: Race):
        self.race = race

    def draw_track(self):
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
        return [self._draw_position(participant) for participant in self.race.participants]

    def _draw_border(self) -> str:
        finish_line_size = 4
        border_size = self.race.distance_to_finish + finish_line_size
        return '+{}+'.format('=' * border_size)

    def _placeholder_participant_lanes(self) -> str:
        linebreak = '\n'
        lanes = linebreak.join(self._draw_lanes(participant) for participant in self.race.participants)
        return lanes

    def _draw_position(self, participant: Participant) -> str:
        if self.race.is_winner(participant):
            path = self._draw_winner_path()
        else:
            path = self._draw_progress_path(participant)
        return path.format(participant.short_name)

    def _draw_winner_path(self) -> str:
        return '|' + (' ' * self.race.distance_to_finish) + '| {} |'

    def _draw_progress_path(self, participant: Participant) -> str:
        progress = '~' * participant.progress
        steps_left = ' ' * self.race.get_steps_left(participant.progress)
        return '|' + progress + "{}" + steps_left + "|   |"

    def _draw_lanes(self, participant) -> str:
        linebreak = '\n'
        placeholder = '{}' + linebreak
        empty_lane = '|{}|   |'.format(' ' * self.race.distance_to_finish)
        return placeholder + empty_lane if self._not_last(participant) else placeholder

    def _not_last(self, participant) -> bool:
        if participant != self.race.participants[-1]:
            return True
