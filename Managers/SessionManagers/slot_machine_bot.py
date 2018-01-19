from Managers.SessionManagers.game_initializer import GameInitializer
from Managers.data_manager import SessionDataManager
from Slots.slot_machine import SlotMachine


class SlotMachineBot(GameInitializer):

    """
    Handles slot games and their payouts.
    """

    def __init__(self, bot, data_manager: SessionDataManager):
        self.bot = bot
        self.data_manager = data_manager

    async def initialize_slots(self, ctx):
        if await self._can_create_game(ctx):
            pass

    async def initialize_bigslots(self, ctx):
        if await self._can_create_game(ctx):
            pass

    async def initialize_giantslots(self, ctx):
        if await self._can_create_game(ctx):
            pass

    async def initialize_mapleslots(self, ctx):
        if await self._can_create_game(ctx):
            pass

    async def initialize_bigmapleslots(self, ctx):
        if await self._can_create_game(ctx):
            pass

    async def initialize_giantmapleslots(self, ctx):
        if await self._can_create_game(ctx):
            pass

    async def _create_session(self, game: SlotMachine):
        self._add_game(game.ctx, game)
        game.run()
        self.save_payout(game)
        await self.report(game)
        self._remove_game(game.ctx)

    async def report(self, slot_machine):
        host_name = slot_machine.get_host_name()
        report = '\n'.join([f"{host_name}'s slot results",
                            slot_machine.get_outcome_report()])
        await self.bot.say(slot_machine.render_slots())
        await self.bot.say(report)

    def save_payout(self, slot_machine):
        user = slot_machine.get_host()
        gold_amount = slot_machine.get_payout_amount()
        if gold_amount != 0:
            self.data_manager.update_gold(user, gold_amount)