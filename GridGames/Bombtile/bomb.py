import asyncio
import random
from typing import List

from Core.constants import GAME_ID
from Core.core_game_class import GameCore
from Core.helper_functions import roll
from GridGames.Bombtile.feedback import BombtileFeedback
from GridGames.Bombtile.player import BombtilePlayer
from GridGames.ScratchCard.constants import *
from GridGames.grid import GridHandler


class Bombtile(GameCore):

    """
    A game where players take turns revealing tiles.
    Most tiles are empty, with several containing multipliers that increase your wager (and therefore
    increase your payout or loss).
    If a player reveals the "bomb" tile, they lose their wager to the rest of the players.
    AFKing in this game is a loss.
    """

    def __init__(self, ctx, bot):
        super().__init__(ctx)
        self.title = "round of Bombtile"
        self.bot = bot
        self.min_players = 2
        self.max_players = 5
        self.num_cells = None  # TBD
        self.num_columns = None  # TBD
        self.num_rows = None  # TBD
        self.grid_values = []  # The hidden tile values.
        self.grid_handler = None  # TBD
        self.visible_grid = []  # The tiles that users see.
        self._payouts = []
        self.feedback = None  # TBD -- Relies on grid dimensions.
        self.id = GAME_ID["BOMBTILE"]

    def add_user(self, user):
        player = BombtilePlayer(user)
        super().add_player(player)
        super().add_user(user)

    async def start_game(self):
        if self.__can_start_game():
            self.__initialize_grid()
            await self.__initialize_feedback()
            super().start_game()
            await self.__report_next_turn()
        else:
            await self.bot.say("Bombtile needs at least two players to start.")

    async def flip(self, coordinates):
        """
        The player action that reveals a tile.
        """
        y = coordinates[0]
        x = coordinates[1]
        tile = self.__reveal_tile(y, x)
        await self.__render_grid()
        await self.__check_multiplier(tile)
        await self.__check_game_end(tile)

    def get_grid_handler(self):
        return self.grid_handler

    def get_payouts(self):
        return self._payouts

    def is_turn(self, user) -> bool:
        return user == self.__get_current_player().user

    def requeue_player(self):
        # If the game is not over, put the player at the end of the queue after their turn.
        player = self.players.pop(0)
        self.players.append(player)

    def is_flippable_tile(self, coordinates: List[int]) -> bool:
        y = coordinates[0]
        x = coordinates[1]
        return self.visible_grid[y][x] is NEUTRAL_TILE

    async def __initialize_feedback(self):
        self.feedback = BombtileFeedback(self)
        welcome = self.feedback.get_starting_message()
        await self.bot.say(welcome)

    async def __render_grid(self):
        await self.bot.say(self.feedback.get_card())

    def __get_current_player(self):
        return self.players[0]

    def __can_start_game(self) -> bool:
        num_players = len(self.players)
        return num_players >= 2

    def __initialize_grid(self):
        # Number of cells in the grid are dependent on the number of players.
        self.num_cells = 3 * len(self.players)
        self.__initialize_grid_dimensions()
        self.grid_handler = GridHandler(self.num_columns, self.num_rows)
        self.__initialize_values()
        self.__initialize_visible_tiles()

    def __initialize_visible_tiles(self):
        # All tiles start blank to the users.
        values = []
        for i in range(self.num_cells):
            values.append(NEUTRAL_TILE)
        self.visible_grid = self.grid_handler.generate_grid(values)

    def __initialize_grid_dimensions(self):
        """
        The grid tends to be wider than it is tall.
        """
        if len(self.players) > 3:
            self.num_columns = len(self.players)
            self.num_rows = self.num_cells // len(self.players)
        else:
            self.num_columns = self.num_cells // len(self.players)
            self.num_rows = len(self.players)

    def __initialize_values(self):
        self.grid_values.append(BOMB)
        self.__add_multipliers()
        self.__add_empty_tiles()
        random.shuffle(self.grid_values)
        self.grid_values = self.grid_handler.generate_grid(self.grid_values)

    def __add_empty_tiles(self):
        tiles_remaining = self.num_cells - len(self.grid_values)
        for i in range(tiles_remaining):
            self.grid_values.append(EMPTY_TILE)

    async def __check_multiplier(self, tile):
        if tile is not BOMB and tile is not EMPTY_TILE:
            multiplier = tile['value']
            self.__get_current_player().update_multiplier(multiplier)
            await self.__report_multiplier(multiplier)

    async def __report_multiplier(self, multiplier):
        player = self.__get_current_player()
        await self.bot.say(self.feedback.get_multiplier_message(player, multiplier))

    async def __check_game_end(self, tile):
        if tile is BOMB:
            await self.__report_loss()
            super().end_game()
            await self.__resolve_payouts()
        else:
            self.requeue_player()
            await self.__report_next_turn()

    async def __report_next_turn(self):
        player = self.__get_current_player()
        message = self.feedback.get_turn(player)
        await self.bot.say(message)

    async def __report_loss(self):
        loser = self.__get_current_player()
        await self.bot.say(self.feedback.get_bomb_report(loser))
        await asyncio.sleep(1.0)

    async def __resolve_payouts(self):
        loser = self.players.pop(0)
        from_user = loser.user.id
        for player in self.players:
            to_user = player.user.id
            amount = player.wager * player.get_multiplier() * loser.get_multiplier()
            await self.report_win(player, amount)
            self.__add_payout(to_user, amount, from_user)

    async def report_win(self, winner: BombtilePlayer, amount: int) -> None:
        report = self.feedback.get_payout_report(winner, amount)
        await self.bot.say(report)

    def __add_payout(self, to_user, amount, from_user) -> None:
        self._payouts.append({
            'to_user': to_user,
            'amount': amount,
            'from_user': from_user
        })

    def __reveal_tile(self, y, x):
        self.visible_grid[y][x] = self.grid_values[y][x]
        return self.grid_values[y][x]

    def __add_multipliers(self):
        """
        Multiplier tiles multiply your wager by the shown amount.
        Eg. if you reveal a TWO tile, you could lose x2 more gold, or win x2 more gold.
        """
        num_players = len(self.players)
        num_multipliers = random.randint(num_players - 1, num_players)
        for i in range(num_multipliers):
            self.__add_random_multiplier()

    def __add_random_multiplier(self):
        possible_multipliers = [TWO, TWO, TWO, THREE, THREE, FIVE]
        multiplier = roll(possible_multipliers)
        self.grid_values.append(multiplier)