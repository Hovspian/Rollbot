from Managers.GameManagers.game_manager import GameManager
from CardGames.blackjack_executor import BlackjackExecutor
from constants import *
from helper_functions import roll
import asyncio


class BlackjackBot(GameManager):

    # Game input, creation and deletion for Blackjack

    def __init__(self, bot):
        super().__init__(bot)

    async def create_blackjack(self, ctx):
        blackjack = BlackjackExecutor(self.bot, ctx)
        self.add_game(blackjack)
        return blackjack

    async def run(self, blackjack: BlackjackExecutor):
        ctx = blackjack.get_context()
        await self.set_join_waiting_period(ctx)
        await self._start_game(blackjack)
        await self._set_game_end(blackjack)

    async def perform_action(self, ctx, action_to_perform: str):
        user = ctx.message.author
        blackjack = await self.get_game(ctx)
        can_make_move = await self.can_make_move(blackjack, user)
        if blackjack and can_make_move:

            actions = {
                "hit": blackjack.hit,
                "stand": blackjack.stand_current_hand,
                "split": blackjack.attempt_split,
                "doubledown": blackjack.attempt_double_down
            }

            await actions[action_to_perform]()

    async def can_make_move(self, game: BlackjackExecutor, user) -> bool:
        move_error = self._check_move_error(game, user)
        if move_error:
            await self.bot.say(move_error)
        else:
            return True

    def _check_move_error(self, game, user) -> any:
        error = False
        if not self._is_in_game(game, user):
            error = "You aren't in the game. Join the next one?"
        elif not self._is_turn(game, user):
            error = "It's not your turn. Please wait."
        elif not game.in_progress:
            error = "The game is not underway yet."
        return error

    @staticmethod
    def _is_turn(game, user) -> bool:
        first_in_queue = game.get_current_player().user
        return user is first_in_queue

    async def _start_game(self, blackjack: BlackjackExecutor) -> None:
        blackjack.in_progress = True
        dealer = blackjack.dealer_name
        await self.bot.say(f"Starting Blackjack. Your dealer is {dealer}, and plays are made against their hand.")
        await blackjack.start()

    async def get_game(self, ctx):
        game = super().get_game(ctx)
        if game:
            return game
        else:
            await self.bot.say("You aren't part of a Blackjack game. Join the next one?")

    async def _say_setup_message(self, ctx):
        user_name = ctx.message.author.display_name
        setup_message = f"{user_name} is starting a round of Blackjack! Type `/join` in the next 20 seconds to join."
        await self.bot.say(setup_message)

    async def _say_last_call_message(self):
        random_messages = ["Generating a deck from thin air.",
                           "Assembling a precarious house of cards.",
                           "Structuring the deck into a totally legit, static order.",
                           "Getting ready to shoot random cards at players.",
                           "(Not) planning the player's demise with nefarious cheats."]
        random_message = roll(random_messages)
        message = SPACE.join([random_message, "Last call to sign up!"])
        await self.bot.say(message)
