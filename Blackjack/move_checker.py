class BlackjackMoveChecker:

    def __init__(self, bot, game):
        self.bot = bot
        self.game = game

    async def perform_action(self, ctx, action_to_perform: str):
        user = ctx.message.author
        can_make_move = await self._can_make_move(user)
        if can_make_move:
            action_list = self.get_actions()
            await action_list[action_to_perform]()

    def get_actions(self):
        return {
                "hit": self.game.hit,
                "stand": self.game.stand_current_hand,
                "split": self.game.attempt_split,
                "doubledown": self.game.attempt_double_down
                }

    async def _can_make_move(self, user) -> bool:
        move_error = self._check_move_error(user)
        if move_error:
            await self.bot.say(move_error)
        else:
            return True

    def _check_move_error(self, user) -> any:
        error = False
        if not self._is_valid_turn(user):
            error = "It's not your turn. Please wait."
        elif not self.game.in_progress:
            error = "The game is not underway yet."
        return error

    def _is_valid_turn(self, user) -> bool:
        first_in_queue = self.game.get_current_player().user
        return user is first_in_queue
