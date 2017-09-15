from HammerRace.race import Race
from HammerRace.participant import Participant


class HammerRaceManager:
    # Manage relationship between feedback, participants and race

    def __init__(self):
        self.race = Race()
        self.race_in_progress = True

    def init_participant(self, short_name: str, name: str):
        participant = Participant(short_name, name)
        self.race.add_participant(participant)
        return participant

    def next_round(self) -> None:
        [self.participant_turn(participant) for participant in self.race.participants]
        self.check_race_end()

    def participant_turn(self, participant: Participant) -> None:
        participant.make_move()
        if self.race.is_winner(participant):
            self.race.add_winner(participant)

    def check_race_end(self) -> None:
        if self.race.is_race_end():
            self.race_in_progress = False

    def round_report(self) -> str:
        race_track = self.race.get_race_track()
        participant_slots = self.race.get_participant_slots()
        return race_track.format(*participant_slots)

    def winner_report(self) -> str:
        winners = self.race.get_winner_name_list()
        if self.race.has_multiple_winners():
            return "The winners are {}".format(winners)
        return "The winner is {}".format(winners)
