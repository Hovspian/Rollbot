import random

from Managers.SessionManagers.game_initializer import GameInitializer, SessionOptions
from MesoPlz.meso_plz import MesoPlz

BRONZE_MESOCOIN = '<:meso:462770303983026196>'
GOLD_MESOCOIN = '<:mesocoin:246852286914101248>'
MESO_WAD = '<:mesowad:246852286993793025>'
MESO_BAG = '<:mesobag:246852286658248704>'


class MesoPlzBot(GameInitializer):
    def __init__(self, options: SessionOptions):
        super().__init__(options)
        self.bot = options.bot
        self.data_manager = options.data_manager

    async def mesos_plz(self, ctx) -> None:
        await self._create_session(MesoPlz(ctx))

    async def _create_session(self, meso_plz: MesoPlz):
        self._add_game(meso_plz.ctx, meso_plz)
        meso_plz.run()
        await self._report(meso_plz)
        self._remove_game(meso_plz.ctx)
        self._save_payout(meso_plz)

    async def _report(self, meso_plz: MesoPlz) -> None:
        mesos = meso_plz.get_payout()
        if mesos == 0:
            await self.__report_no_mesos(meso_plz.ctx)
        elif mesos == 1:
            await meso_plz.ctx.send(f"{BRONZE_MESOCOIN} {mesos} meso")
        elif 2 <= mesos <= 19:
            await meso_plz.ctx.send(f"{BRONZE_MESOCOIN} {mesos} mesos")
        elif 20 <= mesos <= 49:
            await meso_plz.ctx.send(f"{GOLD_MESOCOIN} {mesos} mesos")
        elif 50 <= mesos <= 99:
            await meso_plz.ctx.send(f"{MESO_WAD} {mesos} mesos")
        elif 100 <= mesos <= 250:
            await meso_plz.ctx.send(f"{MESO_BAG} {mesos} mesos")
        else:
            await meso_plz.ctx.send(f"{MESO_BAG}{MESO_BAG} {mesos} mesos")

    async def __report_no_mesos(self, ctx):
        """
        50/50 chance to say 'ccplz'
        """
        if random.randint(0, 1):
            await ctx.send('ccplz')
        else:
            await ctx.send('No mesos')

    def _save_payout(self, meso_plz: MesoPlz) -> None:
        gold_amount = meso_plz.get_payout()
        if gold_amount != 0:
            to_user = meso_plz.get_host()
            from_rollbot = self.bot.user
            self.data_manager.single_transfer(to_user, gold_amount, from_rollbot)