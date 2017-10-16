from Managers.GameManagers.game_manager import GameManager
from CardGames.blackjack_executor import BlackjackExecutor
from constants import *
import asyncio


class RollbotHost:
    """ A fake host for Blackjack """

    def __init__(self):
        self.display_name = "Rollbot"
        self.gold = 10000


class BlackjackBot(GameManager):
    # Game input, creation and deletion for Blackjack

    def __init__(self, bot):
        super().__init__(bot)

    def create_blackjack(self, ctx):
        game_starter = ctx.message.author
        executor = BlackjackExecutor(self.bot, host=RollbotHost())
        executor.add_user(game_starter)
        self.initialize_game(executor)

    def initialize_game(self, game):
        self.add_game(game)

    async def start_game(self, ctx) -> None:
        game = await self.get_game(ctx)
        game.in_progress = True
        host = game.host_name
        await self.bot.say(f"Your dealer is {host}. Starting Blackjack.")
        game.start_game()

    async def perform_action(self, ctx, perform_action: str):
        user = ctx.message.author
        blackjack = await self.get_game(ctx)
        if blackjack and self.can_make_move(blackjack, user):
            actions = {
                "hit": blackjack.hit,
                "stand": blackjack.stand,
                "split": blackjack.split,
                "doubledown": blackjack.double_down
            }

            actions[perform_action]()

    def can_make_move(self, game: BlackjackExecutor, user):
        user_in_game = self.check_in_game(game, user)
        valid_turn = self.check_turn(game, user)
        return user_in_game and valid_turn

    async def check_in_game(self, game, user):
        if self.is_in_game(game, user):
            return True
        else:
            await self.bot.say("You aren't in the game. Join the next one?")

    async def check_turn(self, game, user):
        if self.is_turn(game, user):
            return True
        else:
            current_player_name = game.get_current_player.display_name
            await self.bot.say(f"It's {current_player_name}'s turn.")

    @staticmethod
    def is_in_game(game, user) -> bool:
        return any([player for player in game.players if player.user is user])

    @staticmethod
    def is_turn(game, user) -> bool:
        first_in_queue = game.get_current_player().user
        return user is first_in_queue

    async def requeue_player(self, game):
        first_in_queue = game.players.pop(0)
        player_name = first_in_queue.display_name
        no_player_turns_left = not game.players
        if self.is_past_afk(first_in_queue) or no_player_turns_left:
            await self.bot.say(f"{player_name} is away, and has been removed from the game.")
        else:
            await self.bot.say(f"{player_name} seems to be away. Skipping to the next player...")
            game.players.append(first_in_queue)

    @staticmethod
    async def is_past_afk(player):
        return player.afk > 0

    async def get_game(self, ctx):
        game = super().get_game(ctx)
        if game:
            return game
        else:
            await self.bot.say("This channel doesn't have a round of Blackjack going.")

    async def _medium_time_warning(self, game):
        await self.bot.say(f"One minute left.")

    async def _low_time_warning(self, game):
        await self.bot.say(f"20 seconds left!")

    async def _time_out(self, game):
        await self.bot.say(f"Time limit elapsed. The game has ended.")
        game.in_progress = False

    async def set_join_waiting_period(self, ctx):
        await self.say_setup_message(ctx)
        await asyncio.sleep(5)
        await self.say_blackjack_rules()
        await asyncio.sleep(10)
        await self.say_last_call_message()
        await asyncio.sleep(5)

    async def say_blackjack_rules(self):
        options = ["Blackjack commands:",
                   "`/hit` : Receive a card. If your hand's value exceeds 21 points, it's a bust.",
                   "`/stand` : End your turn with your hand as-is."
                   "`/doubledown` : Double your wager, receive one more card, and stand.",
                   "`/split` : If you are dealt two cards of equal value, split them into separate hands."]
        await self.bot.say(LINEBREAK.join(options))

    async def say_setup_message(self, ctx):
        user_name = ctx.message.author.display_name
        setup_message = f"{user_name} is starting a round of Blackjack! Type /join in the next 20 seconds to join."
        await self.bot.say(setup_message)

    async def say_last_call_message(self):
        await self.bot.say("Generating a deck from thin air. Last call to sign up!")
