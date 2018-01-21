from Core.constants import *
from HammerRace.participant import Participant


class RaceTrack:
    # Draw race track and participant strings
    def __init__(self, race):
        self.race = race

    def draw_track(self) -> str:
        track_frame = self._get_race_track_frame()
        participant_slots = self._get_participant_slots()
        return track_frame.format(participant_slots)

    def _get_race_track_frame(self) -> str:
        track_border = self._draw_border()
        race_track_list = [CODE_TAG,
                           track_border,
                           '{}',
                           track_border,
                           CODE_TAG]
        return LINEBREAK.join(race_track_list)

    def _get_participant_slots(self) -> str:
        lane_list = [self._draw_lanes(player) for player in self.race.players]
        return LINEBREAK.join(lane_list)

    def _draw_border(self) -> str:
        finish_line_size = 4
        wall_size = self.race.distance_to_finish + finish_line_size
        wall = '=' * wall_size
        return f'+{wall}+'

    def _draw_lanes(self, participant: Participant) -> str:
        participant_lane = self._draw_position(participant)
        spacer = ' ' * self.race.distance_to_finish
        empty_lane = f'|{spacer}|   |'

        def final_participant() -> bool:
            return participant == self.race.players[-1]

        return participant_lane if final_participant() else LINEBREAK.join([participant_lane, empty_lane])

    def _draw_position(self, participant: Participant) -> str:
        if self.race.is_winner(participant):
            return self._draw_winner_path(participant)
        return self._draw_progress_path(participant)

    def _draw_winner_path(self, participant: Participant) -> str:
        spacer = SPACE * self.race.distance_to_finish
        short_name = participant.short_name
        return f'|{spacer}| {short_name} |'

    def _draw_progress_path(self, participant: Participant) -> str:
        progress = '~' * participant.progress
        steps_left = SPACE * self.race._get_steps_left(participant.progress)
        short_name = participant.short_name
        return f'|{progress}{short_name}{steps_left}|   |'
