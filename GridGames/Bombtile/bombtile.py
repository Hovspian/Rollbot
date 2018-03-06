import random
from typing import List

from Core.constants import GAME_ID
from Core.core_game_class import GameCore
from Core.helper_functions import roll
from Core.turn_timer import TurnTimer
from GridGames.Bombtile.announcer import BombtileAnnouncer
from GridGames.Bombtile.player import BombtilePlayer
from GridGames.ScratchCard.constants import *
from GridGames.grid import GridHandler


class Bombtile(GameCore):

    """
    A game where players take turns revealing tiles.
    Most tiles are empty, with several containing multipliers that increase your wager (and therefore
    increase your payout or loss).
    If a player reveals the "bomb" tile, they lose their wager to the rest of the players.
    """

    def __init__(self, ctx, bot):
        super().__init__(ctx)
        self.bot = bot
        self.title = "game of Bombtile"
        self.id = GAME_ID["BOMBTILE"]
        self._turn_timer = TurnTimer(bot, self)
        self.min_players = 2
        self.max_players = 5
        self.grid_values = []  # The hidden tile symbols.
        self.visible_grid = []  # The tiles that users see.
        self._payouts = []
        self.num_cells = None  # TBD -- Depends on number of players.
        self.num_columns = None  # TBD
        self.num_rows = None  # TBD
        self.grid_handler = None  # TBD
        self.announcer = None  # TBD -- Relies on grid dimensions.

    def add_user(self, user) -> None:
        player = BombtilePlayer(user)
        super().add_player(player)
        super().add_user(user)

    def is_max_num_players(self) -> bool:
        return len(self.players) == self.max_players

    async def run(self) -> None:
        if self.__can_start_game():
            self.__initialize_grid()
            # Grid dimensions are a dependency of feedback, because feedback uses a string representation of the grid.
            # Hence the ordering.
            await self.__initialize_feedback()
            super().start_game()
            await self.announcer.announce_current_turn()
            await self._turn_timer.run()
        else:
            await self.bot.say("Bombtile needs at least two players to start.")

    async def flip(self, coordinates) -> None:
        """
        The player action that reveals a tile.
        """
        y = coordinates[0]
        x = coordinates[1]
        tile = self.__reveal_tile(y, x)
        await self.announcer.render_grid()
        await self.__check_multiplier(tile)
        await self.__check_game_end(tile)

    def get_payouts(self) -> List[dict]:
        return self._payouts

    def is_turn(self, user) -> bool:
        return user == self.get_current_player().user

    async def resolve_afk(self) -> None:
        await self.announcer.announce_afk()
        await self.__auto_flip_tile()

    def is_flippable_tile(self, coordinates: List[int]) -> bool:
        y = coordinates[0]
        x = coordinates[1]
        return self.visible_grid[y][x] is NEUTRAL_TILE

    def get_current_player(self) -> BombtilePlayer:
        return self.players[0]

    async def __initialize_feedback(self) -> None:
        self.announcer = BombtileAnnouncer(self)
        await self.announcer.announce_start()

    def __can_start_game(self) -> bool:
        num_players = len(self.players)
        return num_players >= 2

    def __initialize_grid(self) -> None:
        # Number of cells in the grid are dependent on the number of players.
        self.num_cells = 3 * len(self.players)
        self.__initialize_grid_dimensions()
        self.__initialize_tile_values()
        self.__initialize_visible_tiles()

    def __initialize_visible_tiles(self) -> None:
        # All tiles start blank to the users.
        tiles = []
        for i in range(self.num_cells):
            tiles.append(NEUTRAL_TILE)
        self.visible_grid = self.grid_handler.generate_grid(tiles)

    def __initialize_grid_dimensions(self) -> None:
        """
        The grid tends to be wider than it is tall.
        """
        if len(self.players) > 3:
            self.num_columns = len(self.players)
            self.num_rows = self.num_cells // len(self.players)
        else:
            self.num_columns = self.num_cells // len(self.players)
            self.num_rows = len(self.players)
        self.grid_handler = GridHandler(self.num_columns, self.num_rows)

    def __initialize_tile_values(self) -> None:
        self.grid_values.append(BOMB)
        self.__add_multipliers()
        self.__add_empty_tiles()
        random.shuffle(self.grid_values)
        self.grid_values = self.grid_handler.generate_grid(self.grid_values)

    def __add_empty_tiles(self) -> None:
        tiles_remaining = self.num_cells - len(self.grid_values)
        for i in range(tiles_remaining):
            self.grid_values.append(EMPTY_TILE)

    async def __check_multiplier(self, tile) -> None:
        if tile is not BOMB and tile is not EMPTY_TILE:
            #  Then the tile must be a multiplier
            multiplier = tile['value']
            self.get_current_player().update_multiplier(multiplier)
            await self.announcer.announce_multiplier()

    async def __check_game_end(self, tile) -> None:
        if tile is BOMB:
            await self.end_game()
        else:
            await self.__next_turn()

    async def end_game(self) -> None:
        await self.announcer.report_loss()
        await self.__resolve_payouts()
        super().end_game()

    async def __next_turn(self) -> None:
        self.__requeue_player()
        self._turn_timer.refresh_turn_timer()
        if await self.__is_final_tile():
            return
        await self.announcer.announce_current_turn()

    async def __auto_flip_tile(self) -> None:
        """
        Flips a random neutral tile.
        """
        valid_tiles = self.__get_neutral_tiles()
        random_tile = roll(valid_tiles)
        await self.flip(random_tile)

    def __get_neutral_tiles(self) -> List[List[int]]:
        """
        Get a list of all indices for flippable tiles.
        """
        neutral_tiles = []
        for x in range(self.num_columns):
            for y in range(self.num_rows):
                if self.is_flippable_tile([y, x]):
                    neutral_tiles.append([y, x])
        return neutral_tiles

    def __requeue_player(self) -> None:
        # If the game is not over, put the player at the end of the queue after their turn.
        player = self.players.pop(0)
        self.players.append(player)

    async def __is_final_tile(self) -> bool:
        """
        If a player is stuck with the last remaining tile, it gets auto flipped on their turn.
        """
        tiles = self.__get_neutral_tiles()
        if len(tiles) == 1:
            player = self.get_current_player()
            await self.announcer.auto_reveal(player)
            await self.flip(tiles[0])
            return True

    async def __resolve_payouts(self) -> None:
        loser = self.players.pop(0)
        for winner in self.players:
            self.__resolve_payout(winner, loser)

    async def __resolve_payout(self, winner, loser) -> None:
        to_user = winner.user
        amount = winner.wager * winner.get_multiplier() * loser.get_multiplier()
        from_user = loser.user
        await self.announcer.report_payout(winner, amount)
        self.__add_payout(to_user, amount, from_user)

    def __add_payout(self, to_user, amount: int, from_user) -> None:
        self._payouts.append({
            'to_user': to_user,
            'amount': amount,
            'from_user': from_user
        })

    def __reveal_tile(self, y: int, x: int) -> dict:
        self.visible_grid[y][x] = self.grid_values[y][x]
        return self.grid_values[y][x]

    def __add_multipliers(self) -> None:
        """
        Multiplier tiles multiply your wager by the shown amount.
        Eg. if you reveal a TWO tile, you could lose x2 more gold, or win x2 more gold.
        """
        num_players = len(self.players)
        num_multipliers = random.randint(num_players - 1, num_players)
        for i in range(num_multipliers):
            self.__add_random_multiplier()

    def __add_random_multiplier(self) -> None:
        possible_multipliers = [TWO, TWO, TWO, THREE, THREE, FIVE]
        multiplier = roll(possible_multipliers)
        self.grid_values.append(multiplier)