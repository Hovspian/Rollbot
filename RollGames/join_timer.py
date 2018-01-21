from Core.join_timer import JoinTimer


class RollGameJoinTimer(JoinTimer):

    def __init__(self, bot, game):
        super().__init__(bot, game)

    async def _say_setup_message(self):
        host = self.game.host_name
        bet = self.game.bet
        game_title = self.game.title
        temp_message = await self.bot.say(f"{host} is creating a {game_title} with {bet}g bet. "
                                          f"Type /join in the next {self.join_time} seconds to join.")
        self.messages_to_cleanup.append(temp_message)


class NormalRollJoinTimer(JoinTimer):

    def __init__(self, bot, game):
        super().__init__(bot, game)

    async def _say_start_message(self):
        await self.bot.say("Start rolling from 1-100.")


class DifferenceRollJoinTimer(JoinTimer):

    def __init__(self, bot, game):
        super().__init__(bot, game)

    async def _say_start_message(self):
        bet = self.game.bet
        await self.bot.say(f"Start rolling from 1-{bet}.")


class CountdownRollJoinTimer(JoinTimer):

    def __init__(self, bot, game):
        super().__init__(bot, game)

    async def _say_start_message(self):
        bet = self.game.bet
        await self.bot.say(f"Roll from 1-{bet}. Then, continue rolling from the player's previous roll.")