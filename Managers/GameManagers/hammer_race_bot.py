import asyncio
from HammerRace.hammer_modes import *
from Managers.GameManagers.game_manager import GameManager
from Managers.data_manager import SessionDataManager


class HammerRaceBot(GameManager):
    def __init__(self, bot):
        super().__init__(bot)

    def create_askhammer(self, ctx) -> ClassicHammer:
        askhammer = ClassicHammer(ctx)
        self.add_game(askhammer)
        return askhammer

    def create_comparisonhammer(self, ctx) -> ComparisonHammer:
        comparison_hammer = ComparisonHammer(ctx)
        self.add_game(comparison_hammer)
        return comparison_hammer

    def create_versushammer(self, ctx) -> VersusHammer:
        versus_hammer = VersusHammer(ctx)
        self.add_game(versus_hammer)
        return versus_hammer

    async def run(self, hammer_race) -> None:
        if hammer_race.valid_num_participants():
            await self._say_start_message(hammer_race)
            await self._run_race(hammer_race)
            self._end_game(hammer_race)
        else:
            await self.bot.say(hammer_race.invalid_participants_error)

    async def _say_setup_message(self, ctx) -> None:
        host_name = ctx.message.author.display_name
        setup_message = f"{host_name} is starting a race. Type /join in the next 20 seconds to join."
        await self.bot.say(setup_message)

    async def _say_start_message(self, hammer_race) -> None:
        start_message = hammer_race.get_start_message()
        if start_message:
            await self.bot.say(start_message)

    async def _run_race(self, hammer_race) -> None:
        hammer_race.in_progress = True
        await self.bot.say(hammer_race.round_report())

        while hammer_race.in_progress:
            await asyncio.sleep(2.0)
            hammer_race.next_round()
            await self.bot.say(hammer_race.round_report())

        await self.bot.say(hammer_race.winner_report())


class HammerPayoutHandler:
    def __init__(self, game: VersusHammer, data_manager: SessionDataManager):
        self.game = game
        self.data_manager = data_manager

    def resolve_payouts(self) -> None:
        for loser in self.game.losers:
            gold_amount = loser['gold']
            divided_amount = loser['divided_gold']
            self.pay_winners(divided_amount)
            self.data_manager.update_gold(loser, -gold_amount)

    def pay_winners(self, gold_amount) -> None:
        for winner in self.game.winners:
            self.data_manager.update_gold(winner, gold_amount)