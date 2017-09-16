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
        return self.race_track.draw_track()

    def get_steps_left(self, progress: int) -> int:
        character_space = 1
        return self.distance_to_finish - progress - character_space

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

    def draw_track(self) -> str:
        track_frame = self._get_race_track_frame()
        participant_slots = self._get_participant_slots()
        return track_frame.format(participant_slots)

    def _get_race_track_frame(self) -> str:
        linebreak = '\n'
        code_tag = '```'
        track_border = self._draw_border()
        race_track_list = [code_tag,
                           track_border,
                           '{}',
                           track_border,
                           code_tag]
        return linebreak.join(race_track_list)

    def _get_participant_slots(self) -> str:
        linebreak = '\n'
        lane_list = [self._draw_lanes(participant) for participant in self.race.participants]
        return linebreak.join(lane_list)

    def _draw_border(self) -> str:
        finish_line_size = 4
        wall_size = self.race.distance_to_finish + finish_line_size
        wall = '=' * wall_size
        return f'+{wall}+'

    def _draw_lanes(self, participant: Participant) -> str:
        linebreak = '\n'
        participant_lane = self._draw_position(participant)
        spacer = ' ' * self.race.distance_to_finish
        empty_lane = f'|{spacer}|   |'

        def final_participant() -> bool:
            return participant == self.race.participants[-1]

        return participant_lane if final_participant() else linebreak.join([participant_lane, empty_lane])

    def _draw_position(self, participant: Participant) -> str:
        if self.race.is_winner(participant):
            return self._draw_winner_path(participant)
        return self._draw_progress_path(participant)

    def _draw_winner_path(self, participant: Participant) -> str:
        spacer = ' ' * self.race.distance_to_finish
        short_name = participant.short_name
        return f'|{spacer}| {short_name} |'

    def _draw_progress_path(self, participant: Participant) -> str:
        progress = '~' * participant.progress
        steps_left = ' ' * self.race.get_steps_left(participant.progress)
        short_name = participant.short_name
        return f'|{progress}{short_name}{steps_left}|   |'
