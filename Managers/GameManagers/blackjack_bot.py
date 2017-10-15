from Managers.GameManagers.game_manager import GameManager
from CardGames.blackjack_executor import BlackjackExecutor


class BlackjackBot(GameManager):

    # Game creation and deletion for Blackjack

    def __init__(self, bot):
        super().__init__(bot)

    def create_blackjack(self, ctx):
        game_starter = ctx.message.author
        blackjack_machine = BlackjackExecutor(self.bot)
        blackjack_machine.add_user(game_starter)
        self.initialize_game(blackjack_machine)

    def initialize_game(self, game):
        self.add_game(game)

    @staticmethod
    def is_turn(game, player) -> bool:
        first_in_queue = game.players[0]
        return player is first_in_queue

    async def requeue_player(self, game):
        first_in_queue = game.players.pop(0)
        player_name = first_in_queue.display_name
        if self.is_past_afk(first_in_queue):
            await self.bot.say(f"{player_name} is away, and has been removed from the game.")
        else:
            await self.bot.say(f"{player_name} seems to be away. Skipping to the next player...")
            game.players.append(first_in_queue)

    @staticmethod
    async def is_past_afk(player):
        return player.afk > 0

