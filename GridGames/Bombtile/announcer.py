import asyncio

from Core.constants import LINEBREAK
from GridGames.grid_renderer import CardRenderer


class BombtileAnnouncer:
    """
    Bot message reports for the state of the Bombtile game.
    """

    def __init__(self, bombtile):
        self.bombtile = bombtile
        self.renderer = CardRenderer(bombtile)
        self.bot = bombtile.bot

    async def render_grid(self) -> None:
        grid = self.renderer.render_grid()
        await self.bot.say(grid)

    async def announce_start(self) -> None:
        starting_message = LINEBREAK.join([':bomb: Welcome to Bombtile! :bomb:',
                                           self.renderer.render_grid(),
                                           'Players take turns flipping tiles. Whoever gets the bomb `<!>` loses!'])
        await self.bot.say(starting_message)

    async def announce_multiplier(self) -> None:
        player = self.bombtile.get_current_player()
        multiplier = player.get_multiplier()
        wager = player.get_wager()
        message = f"{player.name} revealed a x{multiplier} multiplier! " \
                  f"Their {wager} gold wager is multiplied."
        await self.bot.say(message)

    async def report_payout(self, winner, amount: int) -> None:
        # Amount is calculated at the end of the game.
        multiplier = winner.get_multiplier()
        if multiplier > 1:
            message = f":dollar: :dollar: {winner.name} won {amount} gold. " \
                      f"({multiplier}x multiplier) :dollar: :dollar:"
        else:
            message = f":dollar: {winner.name} won {amount} gold. :dollar:"
        await self.bot.say(message)

    async def announce_current_turn(self):
        player = self.bombtile.get_current_player()
        await self.bot.say(f"It's {player.name}'s turn to `/flip` a tile.")

    async def report_loss(self) -> None:
        loser = self.bombtile.get_current_player()
        multiplier = loser.get_multiplier()
        if multiplier > 1:
            message = f":bomb: :bomb: {loser.name} hit the bomb `<!>` with a {multiplier}x multiplier! :bomb: :bomb: "
        else:
            message = f":bomb: {loser.name} hit the bomb `<!>`! :bomb:"
        await self.bot.say(message)

    async def auto_reveal(self, player) -> None:
        await self.bot.say(f"Automatically revealing the last tile for {player.name}...")
        await asyncio.sleep(1.0)

    async def announce_afk(self) -> None:
        player = self.bombtile.get_current_player()
        await self.bot.say(f"{player.name} seems to be away.")
        await asyncio.sleep(1.0)

