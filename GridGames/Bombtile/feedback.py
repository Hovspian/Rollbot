from Core.constants import LINEBREAK
from GridGames.grid_renderer import CardRenderer


class BombtileFeedback:

    """
    Returns string messages for use in Bombtile bot.say() announcements.
    """

    def __init__(self, bombtile):
        self.renderer = CardRenderer(bombtile)

    def get_card(self) -> str:
        return self.renderer.render_card()

    def get_starting_message(self) -> str:
        starting_message = [':bomb: Welcome to Bombtile! :bomb:',
                            self.renderer.render_card(),
                            'Players take turns `/flip`ing tiles. Whoever gets the bomb `<!>` loses!']
        return LINEBREAK.join(starting_message)

    def get_multiplier_message(self, player, multiplier: int) -> str:
        wager = player.get_wager()
        return f"{player.name} revealed a x{multiplier} multiplier! " \
               f"Their {wager} gold wager is multiplied."

    def get_payout_report(self, winner, amount: int) -> str:
        multiplier = winner.get_multiplier()
        if multiplier > 1:
            return f":dollar: :dollar: {winner.name} has a x{multiplier} multiplier!" \
                   f" {winner.name} won {amount} gold. :dollar: :dollar:"
        return f":dollar: {winner.name} won {amount} gold. :dollar:"

    def get_turn(self, player) -> str:
        return f"It's {player.name}'s turn to `/flip` a tile."

    def get_bomb_report(self, loser) -> str:
        multiplier = loser.get_multiplier()
        if multiplier > 1:
            return f":bomb: :bomb: {loser.name} hit the bomb `<!>` with a x{multiplier} multiplier! :bomb: :bomb: "
        return f":bomb: {loser.name} hit the bomb `<!>`! :bomb:"
