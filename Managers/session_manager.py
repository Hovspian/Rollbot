import asyncio
from Managers.channel_manager import *
from Managers.GameManagers.hammer_race_bot import HammerRaceBot
from Managers.GameManagers.scratch_card_bot import ScratchCardBot
from Managers.GameManagers.blackjack_bot import BlackjackBot
from Managers.GameManagers.roll_game_bot import RollGameBot
from GridGames.ScratchCard.Classic.classic_mode import ClassicScratchCard
from GridGames.ScratchCard.Hammerpot.hammerpot import Hammerpot


class SessionManager:

    # Handles the coupling between channel managers and game managers.
    # Namely, channel managers need to know when the game has ended.

    def __init__(self, bot, data_manager):
        self.bot = bot
        self.data_manager = data_manager
        self.channel_manager = ChannelManager(bot)
        self.scratch_card_bot = ScratchCardBot(bot, data_manager)  # GameManager
        self.hammer_race_bot = HammerRaceBot(bot)  # GameManager
        self.blackjack_bot = BlackjackBot(bot)  # GameManager
        self.roll_game_bot = RollGameBot(bot)  # GameManager

    # Game creation
    async def create_blackjack(self, ctx) -> None:
        if await self._is_valid_new_game(ctx, self.blackjack_bot):
            blackjack = await self.blackjack_bot.create_blackjack(ctx)
            channel = ctx.message.channel
            self.channel_manager.add_game_in_session(channel, blackjack)
            await self.blackjack_bot.run(blackjack)
            self.channel_manager.vacate_channel(channel)

    async def create_scratch_card(self, ctx) -> None:
        if await self._is_valid_new_game(ctx, self.scratch_card_bot):
            scratch_card = ClassicScratchCard(ctx)
            await self._create_scratch_game(ctx, scratch_card)

    async def create_hammerpot(self, ctx) -> None:
        if await self._is_valid_new_game(ctx, self.scratch_card_bot):
            hammerpot = Hammerpot(ctx)
            await self._create_scratch_game(ctx, hammerpot)

    async def askhammer(self, ctx) -> None:
        if await self._is_valid_new_game(ctx, self.hammer_bot):
            race = self.hammer_bot.create_askhammer(ctx)
            self._run_hammer(ctx, race)

    async def comparison_hammer(self, ctx) -> None:
        if await self._is_valid_new_game(ctx, self.hammer_bot):
            race = self.hammer_bot.create_comparisonhammer(ctx)
            await self._run_hammer(ctx, race)

    async def create_versushammer(self, ctx) -> None:
        if await self._is_valid_new_game(ctx, self.hammer_bot):
            race = self.hammer_bot.create_versushammer(ctx)
            await self.hammer_bot.set_join_waiting_period(ctx)
            await self._run_hammer(ctx, race)

    async def create_normal_rollgame(self, ctx, bet) -> None:
        if await self._is_valid_new_game(ctx, self.roll_game_bot):
            game = await self.roll_game_bot.create_normal_rollgame(ctx, bet)
            await self._play_rollgame(ctx, game)

    async def create_difference_rollgame(self, ctx, bet) -> None:
        if await self._is_valid_new_game(ctx, self.roll_game_bot):
            game = await self.roll_game_bot.create_difference_rollgame(ctx, bet)
            await self._play_rollgame(ctx, game)

    async def create_countdown_rollgame(self, ctx, bet) -> None:
        if await self._is_valid_new_game(ctx, self.roll_game_bot):
            game = await self.roll_game_bot.create_countdown_rollgame(ctx, bet)
            await self._play_rollgame(ctx, game)

    async def _play_rollgame(self, ctx, game):
        self.channel_manager.add_game_in_session(game)
        await self.roll_game_bot.set_join_waiting_period(ctx)

        if len(self.roll_game_bot.get_game(ctx).users) > 1:
            await self.roll_game_bot.start_rolls(game)
            self._store_rollgame_result(game)
        else:
            await self.bot.say("Not enough players.")
            self.roll_game_bot.terminate_game(game)

        self.channel_manager.vacate_channel(ctx)

    def _store_rollgame_result(self, game):
        loser_result = game.result[0]
        self.data_manager.update_gold(loser_result[0], loser_result[1])
        for winner_result in game.result[1]:
            self.data_manager.update_gold(winner_result[0], winner_result[1])

    async def join_game(self, ctx):
        user_can_join = await self.channel_manager.check_valid_user(ctx)
        if user_can_join:
            await self.channel_manager.add_user_to_game(ctx)

    async def _create_scratch_game(self, ctx, game) -> None:
        channel = ctx.message.channel
        self.channel_manager.add_game_in_session(channel, game)
        await self.scratch_card_bot.initialize_game(game)
        self.channel_manager.vacate_channel(channel)

    async def _run_hammer(self, ctx, hammer_race):
        channel = ctx.message.channel
        await self.hammer_bot.run(hammer_race)
        self.channel_manager.vacate_channel(channel)

    async def _is_valid_new_game(self, ctx, game_manager) -> bool:
        # Check channel and game manager
        host = ctx.message.author
        valid_channel = await self.channel_manager.check_valid_new_game(ctx)
        valid_user = await game_manager.check_user_game_running(host)
        return valid_channel and valid_user
