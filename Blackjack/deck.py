from copy import deepcopy
from Core.helper_functions import *
from Blackjack.hand import *


class Deck:

    """
    Mechanics involving deck manipulation.
    """

    def __init__(self):
        self.round = 0
        self.default_cards = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        self.suits = [':diamonds:', ':clubs:', ':hearts:', ':spades:']
        self.deck = self.generate_deck()

    def generate_deck(self) -> dict:
        deck = {}
        for suit in self.suits:
            deck[suit] = deepcopy(self.default_cards)
        return deck

    def hit(self, hand: BlackjackHand) -> dict:
        """
        Draw a card as an action.
        """
        card = self._draw_card()
        hand.hit(card)
        return card

    def deal_card(self, hand: BlackjackHand):
        """
        Eg. passing out cards at the start of the game.
        """
        card = self._draw_card()
        hand.add_card(card)

    def double_down(self, hand: PlayerHand) -> bool:
        """
        Double wager, then draw and finish.
        """
        if hand.plays_made == 0:
            hand.double_down(self._draw_card())
            return True

    def _draw_card(self) -> dict:
        # TODO rolling suit which is always 25% chance per suit is off the mark
        suit = roll(self.suits)
        rank = roll(self.deck[suit])
        self.deck[suit].remove(rank)
        card = {'rank': rank, 'suit': suit}
        return card
