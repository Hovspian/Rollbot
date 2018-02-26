import asyncio


class MoveChecker:
    """
    Helper for generic move checking in multiplayer games.
    """

    def __init__(self, bot, game):
        self.game = game
        self.bot = bot

    async def can_make_move(self, user) -> bool:
        move_error = self.__check_move_error(user)
        if move_error is None:
            return True
        temp_message = await self.bot.say(move_error)
        await self.__auto_delete_message(temp_message)

    def __check_move_error(self, user) -> any:
        error = None
        if not self.game.is_turn(user):
            error = "It's not your turn. Please wait."
        elif not self.game.in_progress:
            error = "The game is not underway yet."
        return error

    async def __auto_delete_message(self, message):
        await asyncio.sleep(5.0)
        await self.bot.delete_message(message)