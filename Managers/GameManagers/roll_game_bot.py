from Managers.GameManagers.game_manager import GameManager
from helper_functions import *
from RollGames.roll_game_modes import *


class RollGameBot(GameManager):


    def __init__(self, bot):
        super().__init__(bot)


    async def create_normal_rollgame(self, ctx, bet):
        game = NormalRollGame(self.bot, ctx, bet)
        await game.add(ctx.message.author)
        self.add_game(game)
        return game

    async def create_difference_rollgame(self, ctx, bet):
        game = DifferenceRollGame(self.bot, ctx, bet)
        await game.add(ctx.message.author)
        self.add_game(game)
        return game

    async def create_countdown_rollgame(self, ctx, bet):
        game = CountdownRollGame(self.bot, ctx, bet)
        await game.add(ctx.message.author)
        self.add_game(game)
        return game

    async def start_rolls(self, ctx, game : RollGame):
        game.in_progress = True

        await self.bot.say(game.play_message())

        await self.bot.say("Waiting for rolls")
        await game.wait_for_rolls(game.bet)

        await self.bot.say("Determining results")
        result = await game.determine(game.player_rolls)
        loser = game.get_name(result[0][0])
        winner = game.get_name(result[1][0][0])
        the_difference = result[1][0][1] - result[0][1]
        if the_difference == 0:
            await self.bot.say("It's a tie.")
        else:
            split_winners = ', '.join(winner)
            await self.bot.say(f"{loser} owes {split_winners} {result[2]}g")

        self._store_result(result)

        self._end_game(game)
        game.in_progress = False

    def _store_result(self, result):
        pass

    async def say_setup_message(self, ctx, game):
        await self.bot.say(game.create_message(ctx))

    async def set_join_waiting_period(self, ctx, game):
        await self.say_setup_message(ctx, game)
        await asyncio.sleep(15)
        await self.say_last_call_message()
        await asyncio.sleep(5)