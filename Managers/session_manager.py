from Managers.channel_manager import ChannelManager
from Managers.scratch_card_bot import ScratchCardBot
from Managers.hammer_race_bot import HammerRaceBot
from GridGames.ScratchCard.Classic.classic_mode import ClassicScratchCard
from GridGames.ScratchCard.Hammerpot.hammerpot import Hammerpot
from HammerRace.hammer_modes import *
from helper_functions import *
import asyncio


class SessionManager:

    # Handles the coupling between channel manager and game managers.
    # Namely, channel managers need to know when the game has ended.

    def __init__(self, bot):
        self.bot = bot
        self.channel_manager = ChannelManager(bot)
        self.scratch_card_bot = ScratchCardBot(bot)  # GameManager
        self.hammer_race_bot = HammerRaceBot(bot)  # GameManager

    # Game creation
    async def create_scratch_card(self, ctx) -> None:
        if await self._is_valid_new_game(ctx, self.scratch_card_bot):
            scratch_card = ClassicScratchCard()
            await self._create_scratch_game(ctx, scratch_card)

    async def create_hammerpot(self, ctx) -> None:
        if await self._is_valid_new_game(ctx, self.scratch_card_bot):
            hammerpot = Hammerpot()
            await self._create_scratch_game(ctx, hammerpot)

    async def _create_scratch_game(self, ctx, game) -> None:
        self.channel_manager.add_game_in_session(ctx, game)
        await self.scratch_card_bot.initialize_game(ctx, game)
        game_ended = await self.scratch_card_bot.set_time_limit(game)
        if game_ended:
            self.channel_manager.vacate_channel(ctx)

    async def create_askhammer(self, ctx) -> None:
        if await self._is_valid_new_game(ctx, self.hammer_race_bot):
            question = message_without_command(ctx.message.content)
            hammer_race = ComparisonHammer(question)
            self.channel_manager.add_game_in_session(ctx, game=hammer_race)
            await self.hammer_race_bot.start_race(hammer_race)
            self.channel_manager.vacate_channel(ctx)

    async def create_comparisonhammer(self, ctx) -> None:
        if await self._is_valid_new_game(ctx, self.hammer_race_bot):
            options = message_without_command(ctx.message.content)
            hammer_race = ComparisonHammer(options)
            self.channel_manager.add_game_in_session(ctx, game=hammer_race)
            await self.hammer_race_bot.start_race(hammer_race)
            self.channel_manager.vacate_channel(ctx)

    async def create_versushammer(self, ctx) -> None:
        if await self._is_valid_new_game(ctx, self.hammer_race_bot):
            user = ctx.message.author
            hammer_race = VersusHammer(user)
            self.channel_manager.add_game_in_session(ctx, game=hammer_race)
            await self.setup_competitive_game(game=hammer_race)
            await self.hammer_race_bot.start_race(hammer_race)
            self.channel_manager.vacate_channel(ctx)

    async def setup_competitive_game(self, game):
        setup_message = SPACE.join([game.setup_message, "Type /join in the next 20 seconds to join."])
        await self.bot.say(setup_message)
        await self.set_join_waiting_period()

    async def set_join_waiting_period(self):
        await asyncio.sleep(15)
        await self.bot.say("Starting in 5 seconds. Last call to sign up.")
        await asyncio.sleep(5)

    # Game actions
    async def join_game(self, ctx):
        user_can_join = await self.channel_manager.check_valid_user(ctx)
        if user_can_join:
            await self.channel_manager.add_user_to_game(ctx)

    async def pick_line(self, ctx) -> None:
        action = self.scratch_card_bot.pick_line
        await self._make_scratch_game_action(ctx, action)

    async def scratch(self, ctx) -> None:
        action = self.scratch_card_bot.next_turn
        await self._make_scratch_game_action(ctx, action)

    async def _is_valid_new_game(self, ctx, game_manager) -> bool:
        # Check channel and game manager
        host = ctx.message.author
        valid_channel = await self.channel_manager.check_valid_new_game(ctx)
        valid_user = await game_manager.check_valid_user(host)
        return valid_channel and valid_user

    async def _make_scratch_game_action(self, ctx, action: classmethod) -> None:
        valid_channel_host = await self.channel_manager.is_valid_channel_host(ctx)
        game = await self.scratch_card_bot.get_game(ctx)
        if valid_channel_host and game:
            raw_input = message_without_command(ctx.message.content)
            await action(game, raw_input)