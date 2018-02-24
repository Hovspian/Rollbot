from copy import deepcopy
from Core.helper_functions import *
from Blackjack.hand import *


class Deck:

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

    def draw_card(self) -> dict:
        # TODO rolling suit which is always 25% chance per suit is off the mark
        suit = roll(self.suits)
        rank = roll(self.deck[suit])
        self.deck[suit].remove(rank)
        card = {'rank': rank, 'suit': suit}
        return card
