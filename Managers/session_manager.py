from Managers.channel_manager import ChannelManager
from Managers.scratch_card_bot import ScratchCardBot
from GridGames.ScratchCard.Classic.classic_mode import ClassicScratchCard
from GridGames.ScratchCard.Hammerpot.hammerpot import Hammerpot
from helper_functions import *


class SessionManager:

    # Handles the coupling between channel manager and game managers.
    # Namely, channel managers need to know when the game has ended.

    def __init__(self, bot):
        self.bot = bot
        self.channel_manager = ChannelManager(bot)
        self.scratch_card_bot = ScratchCardBot(bot)  # GameManager

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
        self.channel_manager.add_game_in_progress(ctx, game)
        await self.scratch_card_bot.initialize_game(ctx, game)
        game_ended = await self.scratch_card_bot.set_time_limit(game)
        if game_ended:
            self.channel_manager.vacate_channel(ctx)

    # Game actions
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