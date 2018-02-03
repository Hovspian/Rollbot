from Managers.SessionManagers.game_initializer import GameInitializer, SessionOptions
from Managers.data_manager import SessionDataManager
from Slots.modes import ClassicSlots, BigClassicSlots, GiantClassicSlots, MapleSlots, BigMapleSlots, GiantMapleSlots
from Slots.slot_machine import SlotMachine


class SlotMachineBot(GameInitializer):

    """
    Handles slot games and their payouts.
    """

    def __init__(self, options: SessionOptions):
        super().__init__(options)
        self.bot = options.bot
        self.data_manager = options.data_manager

    def initialize_game(self, ctx):
        pass

    async def initialize_slots(self, ctx):
        if await self._can_create_game(ctx):
            slots = ClassicSlots(ctx)
            await self._create_session(slots)

    async def initialize_bigslots(self, ctx):
        if await self._can_create_game(ctx):
            slots = BigClassicSlots(ctx)
            await self._create_session(slots)

    async def initialize_giantslots(self, ctx):
        if await self._can_create_game(ctx):
            slots = GiantClassicSlots(ctx)
            await self._create_session(slots)

    async def initialize_mapleslots(self, ctx):
        if await self._can_create_game(ctx):
            slots = MapleSlots(ctx)
            await self._create_session(slots)

    async def initialize_bigmapleslots(self, ctx):
        if await self._can_create_game(ctx):
            slots = BigMapleSlots(ctx)
            await self._create_session(slots)

    async def initialize_giantmapleslots(self, ctx):
        if await self._can_create_game(ctx):
            slots = GiantMapleSlots(ctx)
            await self._create_session(slots)

    async def _create_session(self, slots: SlotMachine):
        self._add_game(slots.ctx, slots)
        slots.run()
        self.save_payout(slots)
        await self.report(slots)
        self._remove_game(slots.ctx)

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