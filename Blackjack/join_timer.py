from Core.core_game_class import GameCore
from Core.join_timer import JoinTimer
from Core.constants import *
from Core.helper_functions import roll


class BlackjackJoinTimer(JoinTimer):
    def __init__(self, bot, game):
        super().__init__(bot, game)
        self.random_messages = ["Generating a deck from thin air.",
                                "Assembling a precarious house of cards.",
                                "Structuring the deck into a totally legit, static order.",
                                "Getting ready to shoot random cards at players.",
                                "(Not) planning the player's demise with nefarious cheats."]

    async def _say_setup_message(self):
        user_name = self.game.host_name
        setup_message = f"{user_name} is starting a round of Blackjack!" \
                        f" Type `/join` in the next {self.join_time} seconds to join."
        await self.bot.say(setup_message)

    async def _say_last_call_message(self):
        random_message = roll(self.random_messages)
        last_call = SPACE.join([random_message, "Last call to sign up!"])
        await self.bot.say(last_call)

    async def _say_start_message(self):
        dealer = self.game.dealer.name
        await self.bot.say(f"Starting Blackjack. Your dealer is {dealer}, "
                           "and plays are made against their hand.")
