from Managers.SessionManagers.game_initializer import GameInitializer, SessionOptions
from Slots.modes import ClassicSlots, BigClassicSlots, GiantClassicSlots, MapleSlots, BigMapleSlots, GiantMapleSlots, \
    BigPokeSlots, GiantPokeSlots, PokeSlots
from Slots.slot_machine import SlotMachine


class SlotMachineBot(GameInitializer):

    """
    Handles slot games and their payouts.
    """

    def __init__(self, options: SessionOptions):
        super().__init__(options)
        self.bot = options.bot
        self.data_manager = options.data_manager

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

    async def initialize_pokeslots(self, ctx):
        if await self._can_create_game(ctx):
            slots = PokeSlots(ctx)
            await self._create_session(slots)

    async def initialize_bigpokeslots(self, ctx):
        if await self._can_create_game(ctx):
            slots = BigPokeSlots(ctx)
            await self._create_session(slots)

    async def initialize_giantpokeslots(self, ctx):
        if await self._can_create_game(ctx):
            slots = GiantPokeSlots(ctx)
            await self._create_session(slots)

    async def _create_session(self, slots: SlotMachine):
        self._add_game(slots.ctx, slots)
        slots.run()
        await self._report(slots)
        self._remove_game(slots.ctx)
        self._save_payout(slots)

    async def _report(self, slot_machine):
        host_name = slot_machine.get_host_name()
        report = '\n'.join([f"{host_name}'s slot results",
                            slot_machine.get_outcome_report()])
        await slot_machine.ctx.send(slot_machine.render_slots())
        await slot_machine.ctx.send(report)

    def _save_payout(self, slot_machine):
        to_user = slot_machine.get_host()
        gold_amount = slot_machine.get_payout()
        if gold_amount != 0:
            from_rollbot = self.bot.user
            self.data_manager.single_transfer(to_user, gold_amount, from_rollbot)
