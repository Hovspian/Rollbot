import asyncio

from Blackjack.hand import PlayerHand
from Blackjack.render_card import RenderCard
from Core.constants import *


class BlackjackPlayerAnnouncer:

    """
    Handles blackjack feedback.
    """

    def __init__(self, bot):
        self.bot = bot
        self.renderer = RenderCard()

    async def player_cards(self, player_name, hand: PlayerHand, ctx):
        await asyncio.sleep(1)
        rendered_hand = self.renderer.render_hand(hand)
        await ctx.send(f"Dealt to {player_name}: {rendered_hand}")

    async def player_hand(self, player_name, hand: PlayerHand, ctx):
        await asyncio.sleep(1)
        rendered_hand = self.renderer.render_hand(hand)
        message = f"{player_name}'s hand: {rendered_hand}"
        await ctx.send(message)

    async def next_turn(self, player_name, hand: PlayerHand, ctx):
        rendered_hand = self.renderer.render_hand(hand)
        message = LINEBREAK.join([f"{player_name}'s turn. Your hand is:",
                                  f"{rendered_hand}",
                                  "Options: `/hit`  `/stand`  `/doubledown`  `/split`"])
        await ctx.send(message)

    async def report_hit(self, hand, new_card, ctx):
        rendered_hand = self.renderer.render_hand(hand)
        rendered_new_card = self.renderer.render_card(new_card)
        hand_report = LINEBREAK.join([f"You received: {rendered_new_card}",
                                      f"Your hand: {rendered_hand}"])
        await ctx.send(hand_report)

    async def no_players_left(self, ctx):
        await ctx.send("There are no more competitors left. The game has ended.")

    async def split_successful(self, hand: PlayerHand, ctx):
        await ctx.send("Your cards have been split into two hands.")
        await self.next_hand_options(hand, ctx)

    async def split_fail(self, ctx):
        await ctx.send("You can only split on your starting hand, and only if the cards are the same value.")

    async def double_down_fail(self, ctx):
        await ctx.send("You can only double down as your first action.")

    async def declare_player_bust(self, ctx):
        await ctx.send("It's a bust! The dealer has acquired your wager.")

    async def ask_hit_again(self, ctx):
        await ctx.send("Hit again?")

    async def announce_player_blackjack(self, winnings, ctx):
        await ctx.send(f":moneybag: Blackjack! Payout is {winnings} gold. :moneybag:")

    async def stand_off(self, wager: int, ctx):
        await ctx.send(f"Stand-off with the dealer. Your {wager} gold wager has been returned.")

    async def win(self, winnings: int, ctx):
        await ctx.send(f":dollar: Winner! Payout is {winnings} gold. :dollar:")

    async def loss(self, wager: int, ctx):
        await ctx.send(f"You lost your wager of {wager} gold.")

    async def double_down_success(self, wager, ctx):
        await ctx.send(f"Your wager is now {wager}. A face-down card has been added to your hand.")

    async def progressing(self, ctx):
        await ctx.send("Moving on...")

    async def next_hand_options(self, hand: PlayerHand, ctx):
        """
        For split hands.
        """
        rendered_hand = self.renderer.render_hand(hand)
        message = LINEBREAK.join(["Please make a play:",
                                  f"{rendered_hand}",
                                  "Options: `/hit`  `/stand`  `/doubledown`"])
        await ctx.send(message)

    async def announce_blackjack(self, ctx):
        await ctx.send("Blackjack!")


class BlackjackDealerAnnouncer:

    """
    Methods for announcing blackjack dealer moves.
    """

    def __init__(self, bot, dealer_name):
        self.bot = bot
        self.renderer = RenderCard()
        self.dealer = dealer_name

    async def dealer_card(self, card, ctx):
        rendered_card = self.renderer.render_card(card)
        await ctx.send(f"Dealer's face-up card: {rendered_card}")

    async def dealer_turn(self, hand, ctx):
        dealer_hand = self.__get_dealer_hand_reveal(hand)
        message = LINEBREAK.join(["It's the dealer's turn.", dealer_hand])
        await ctx.send(message)

    async def dealer_hit(self, new_card: dict, ctx):
        rendered_card = self.renderer.render_card(new_card)
        await asyncio.sleep(1)
        await ctx.send(f"{self.dealer} drew {rendered_card}")

    async def declare_dealer_bust(self, ctx):
        await asyncio.sleep(1)
        await ctx.send(f"{self.dealer}'s hand has busted!")

    async def ace_or_ten_message(self, hand, ctx):
        await asyncio.sleep(1)
        await ctx.send(f"{self.dealer} is revealing their other card in case of a blackjack...")
        dealer_hand = self.__get_dealer_hand_reveal(hand)
        await asyncio.sleep(1)
        await ctx.send(dealer_hand)

    async def dealer_stand(self, ctx):
        await asyncio.sleep(1)
        await ctx.send("The dealer is now standing. Comparing hands...")

    def __get_dealer_hand_reveal(self, hand) -> str:
        rendered_hand = self.renderer.render_hand(hand)
        return f"{self.dealer} shows their hand: {rendered_hand}"

    async def announce_blackjack(self, ctx):
        await ctx.send("Blackjack!")
