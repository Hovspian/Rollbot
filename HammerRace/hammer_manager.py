from HammerRace.race import Race
from HammerRace.participant import Participant


class HammerRaceManager:
    # Manage relationship between feedback, participants and race

    def __init__(self):
        self.race = Race()
        self.race_in_progress = True

    def _init_participant(self, short_name: str, name: str):
        participant = Participant(short_name, name)
        self.race.add_participant(participant)
        return participant

    def next_round(self) -> None:
        [self._participant_turn(participant) for participant in self.race.participants]
        self._check_race_end()

    def _participant_turn(self, participant: Participant) -> None:
        participant.make_move()
        if self.race.is_winner(participant):
            self.race.add_winner(participant)

    def _check_race_end(self) -> None:
        if self.race.is_race_end():
            self.race_in_progress = False

    def round_report(self) -> str:
        return self.race.get_full_track()

    def winner_report(self) -> str:
        winners = self.race.get_winner_name_list()
        report = "The winners are {}".format(winners) if self.race.has_multiple_winners() \
            else "The winner is {}".format(winners)
        return report
