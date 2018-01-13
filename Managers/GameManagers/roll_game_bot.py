from Managers.GameManagers.game_manager import GameManager
from helper_functions import *
from RollGames.roll_game_modes import *


class RollGameBot(GameManager):

    def __init__(self, bot, data_manager):
        super().__init__(bot)
        self.data_manager = data_manager

    async def create_normal_rollgame(self, ctx, bet):
        game = NormalRollGame(self.bot, self.data_manager, ctx, bet)
        await game.add_user(ctx.message.author)
        self.add_game(game)
        return game

    async def create_difference_rollgame(self, ctx, bet):
        game = DifferenceRollGame(self.bot, self.data_manager, ctx, bet)
        await game.add_user(ctx.message.author)
        self.add_game(game)
        return game

    async def create_countdown_rollgame(self, ctx, bet):
        game = CountdownRollGame(self.bot, self.data_manager, ctx, bet)
        await game.add_user(ctx.message.author)
        self.add_game(game)
        return game

    async def start_rolls(self, game : RollGame):
        game.in_progress = True

        await self.bot.say(game.play_message())
        await game.wait_for_rolls()
        result = await game.determine()

        if result[0][1] == 0:
            await self.bot.say("It's a tie")
        else:
            loser = game.get_name(result[0][0])
            winners = []
            for tup in result[1]:
                winners.append(game.get_name(tup[0]))
            split_winners = ', '.join(winners)
            await self.bot.say(f"{loser} owes {split_winners} {result[1][0][1]}g")
            self._store_result(result)

        self._end_game(game)
        game.in_progress = False

    def _store_result(self, result):
        loser_result = result[0]
        self.data_manager.update_gold(loser_result[0], loser_result[1])
        for winner_result in result[1]:
            self.data_manager.update_gold(winner_result[0], winner_result[1])

    async def say_setup_message(self, ctx):
        host_name = ctx.message.author.display_name
        setup_message = f"{host_name} is starting a roll game. Type /join in the next 20 seconds to join."
        await self.bot.say(setup_message)

    async def set_join_waiting_period(self, ctx):
        await self.say_setup_message(ctx)
        await asyncio.sleep(1)
        await self.say_last_call_message()
        await asyncio.sleep(1)