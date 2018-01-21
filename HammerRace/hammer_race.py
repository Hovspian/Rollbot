import asyncio
from abc import abstractmethod

from Core.constants import GAME_ID
from Core.helper_functions import message_without_command
from Core.core_game_class import GameCore
from HammerRace.participant import Participant
from HammerRace.race_track import RaceTrack


class HammerRace(GameCore):

    def __init__(self, bot, ctx):
        super().__init__(ctx)
        self.bot = bot
        self.distance_to_finish = 40
        self.winners = []
        self.participants = []  # Participant[]. Participant is Versus's avatar object.
        self.race_track = RaceTrack(self)
        self.message = message_without_command(ctx.message.content)
        self.id = GAME_ID["RACE"]
        self.title = "Race"

    async def run(self) -> None:
        self.start_game()
        await self.bot.say(self._round_report())

        while self.in_progress:
            await asyncio.sleep(2.0)
            self._next_round()
            await self.bot.say(self._round_report())

        await self.bot.say(self._get_outcome_report())

    def valid_num_players(self) -> bool:
        within_min_players = len(self.participants) > 1
        within_max_players = len(self.participants) <= 5
        return within_min_players and within_max_players

    def is_winner(self, participant: Participant) -> bool:
        return self._get_steps_left(participant.progress) <= 0

    def _round_report(self) -> str:
        return self.race_track.draw_track()

    @abstractmethod
    def _get_outcome_report(self) -> str:
        raise NotImplementedError

    def _get_winner_report(self) -> str:
        winners = self._get_winner_names()
        report = "The winners are {}" if self._has_multiple_winners() else "The winner is {}"
        return report.format(winners)

    def _next_round(self) -> None:
        [self._participant_turn(participant) for participant in self.participants]
        self._check_race_end()

    def _init_participant(self, short_name: str, name: str):
        participant = Participant(short_name, name)
        self.participants.append(participant)
        return participant

    def _participant_turn(self, participant: Participant) -> None:
        participant.make_move()
        if self.is_winner(participant):
            self._add_winner(participant)

    def _check_race_end(self) -> None:
        if self.is_race_end():
            self.end_game()

    def _get_steps_left(self, progress: int) -> int:
        character_space = 1
        return self.distance_to_finish - progress - character_space

    def _add_winner(self, participant: Participant) -> None:
        self.winners.append(participant)

    def is_race_end(self) -> bool:
        return len(self.winners) > 0

    def _has_multiple_winners(self) -> bool:
        return len(self.winners) > 1

    def _get_participant_names(self) -> str:
        return ', '.join(participant.name for participant in self.participants)

    def _get_winner_names(self) -> str:
        return ', '.join(winner.name for winner in self.winners)
