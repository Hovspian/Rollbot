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

    def __init__(self, bot):
        self.bot = bot
        self.channel_manager = ChannelManager(bot)
        self.user_manager = UserManager(self.channel_manager, bot)
        self.scratch_card_bot = ScratchCardBot(bot)  # GameManager
        self.hammer_race_bot = HammerRaceBot(bot)  # GameManager
        self.blackjack_bot = BlackjackBot(bot) # GameManager
        self.roll_game_bot = RollGameBot(bot, self)  # GameManager

    # Game creation
    async def create_blackjack(self, ctx) -> None:
        if await self._is_valid_new_game(ctx, self.blackjack_bot):
            blackjack = await self.blackjack_bot.create_blackjack(ctx)
            self.channel_manager.add_game_in_session(ctx, blackjack)
            await self.blackjack_bot.set_join_waiting_period(ctx)
            await self.blackjack_bot.start_game(blackjack)
            game_ended = await self.blackjack_bot.set_time_limit(blackjack)
            if game_ended:
                self.channel_manager.vacate_channel(ctx)

    async def create_scratch_card(self, ctx) -> None:
        if await self._is_valid_new_game(ctx, self.scratch_card_bot):
            user = ctx.message.author
            scratch_card = ClassicScratchCard(host=user)
            await self._create_scratch_game(ctx, scratch_card)

    async def create_hammerpot(self, ctx) -> None:
        if await self._is_valid_new_game(ctx, self.scratch_card_bot):
            user = ctx.message.author
            hammerpot = Hammerpot(host=user)
            await self._create_scratch_game(ctx, hammerpot)

    async def _create_scratch_game(self, ctx, game) -> None:
        self.channel_manager.add_game_in_session(ctx, game)
        await self.scratch_card_bot.initialize_game(ctx, game)
        game_ended = await self.scratch_card_bot.set_time_limit(game)
        if game_ended:
            self.channel_manager.vacate_channel(ctx)

    async def askhammer(self, ctx) -> None:
        if await self._is_valid_new_game(ctx, self.hammer_race_bot):
            hammer_race = self.hammer_race_bot.create_askhammer(ctx)
            self.channel_manager.add_game_in_session(ctx, game=hammer_race)
            await self.hammer_race_bot.start_race(hammer_race)
            self.channel_manager.vacate_channel(ctx)

    async def comparison_hammer(self, ctx) -> None:
        if await self._is_valid_new_game(ctx, self.hammer_race_bot):
            hammer_race = self.hammer_race_bot.create_comparisonhammer(ctx)
            self.channel_manager.add_game_in_session(ctx, game=hammer_race)
            await self.hammer_race_bot.start_race(hammer_race)
            self.channel_manager.vacate_channel(ctx)

    async def create_versushammer(self, ctx) -> None:
        if await self._is_valid_new_game(ctx, self.hammer_race_bot):
            hammer_race = self.hammer_race_bot.create_versushammer(ctx)
            self.channel_manager.add_game_in_session(ctx, game=hammer_race)
            await self.hammer_race_bot.set_join_waiting_period(ctx)
            await self.hammer_race_bot.start_race(hammer_race)
            self.channel_manager.vacate_channel(ctx)

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
        self.channel_manager.add_game_in_session(ctx, game)
        await self.roll_game_bot.set_join_waiting_period(ctx, game)

        if len(self.roll_game_bot.get_game(ctx).users) > 2:
            await self.roll_game_bot.start_rolls(ctx, game)
        else:
            await self.bot.say("Not enough players.")

        self.channel_manager.vacate_channel(ctx)

    async def join_game(self, ctx):
        user_can_join = await self.user_manager.check_valid_user(ctx)
        if user_can_join:
            await self.user_manager.add_user_to_game(ctx)

    async def _is_valid_new_game(self, ctx, game_manager) -> bool:
        # Check channel and game manager
        host = ctx.message.author
        valid_channel = await self.channel_manager.check_valid_new_game(ctx)
        valid_user = await game_manager.check_valid_user(host)
        return valid_channel and valid_user
