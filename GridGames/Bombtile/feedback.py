from Core.constants import LINEBREAK
from GridGames.grid_renderer import CardRenderer


class BombtileFeedback:
    def __init__(self, bombtile):
        self.bombtile = bombtile
        self.renderer = CardRenderer(bombtile)

    def get_card(self) -> str:
        return self.renderer.render_card()

    def get_starting_message(self):
        starting_message = [':bomb: Welcome to Bombtile! :bomb:',
                            self.renderer.render_card(),
                            'Players take turns `/flip`ing tiles. Whoever gets the bomb `<!>` loses!']
        return LINEBREAK.join(starting_message)

    def get_multiplier_message(self, player, multiplier: int):
        wager = player.get_wager()
        return f"{player.name} revealed a x{multiplier} multiplier! " \
               f"Their {wager} gold wager is multiplied."

    def get_payout_report(self, winner, amount: int):
        multiplier = winner.get_multiplier()
        if multiplier > 1:
            return f"{winner.name} has a x{multiplier} multiplier! {winner.name} won {amount} gold."
        return f"{winner.name} won {amount} gold."

    def get_turn(self, player):
        return f"It's {player}'s turn to `/flip` a tile."

    def get_bomb_report(self, loser):
        multiplier = loser.get_multiplier()
        if multiplier > 1:
            return f":bomb: :bomb: {loser.name} hit the bomb `<!>` with a x{multiplier} multiplier!"
        return f":bomb: {loser.name} hit the bomb `<!>`!"
