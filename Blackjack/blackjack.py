from copy import deepcopy
from Core.helper_functions import *
from Blackjack.hand import *


class Blackjack:

    # Internal mechanics

    def __init__(self):
        self.round = 0
        self.default_cards = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        self.values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10,
                       'K': 10}
        self.suits = [':diamonds:', ':clubs:', ':hearts:', ':spades:']
        self.deck = {}
        self.generate_deck()

    def generate_deck(self) -> None:
        for suit in self.suits:
            self.deck[suit] = deepcopy(self.default_cards)

    def hit(self, hand: Hand) -> dict:
        """ Draw a card as an action """
        card = self.draw_card()
        hand.hit(card)
        self.update_hand_value(hand)
        return card

    def deal_card(self, hand: Hand):
        """ Deal a card, eg. at the start of the game. """
        card = self.draw_card()
        hand.add_card(card)
        self.update_hand_value(hand)

    def double_down(self, hand: PlayerHand) -> bool:
        """ Double wager, then draw and finish """
        if hand.plays_made == 0:
            hand.double_down(self.draw_card())
            self.update_hand_value(hand)
            return True

    def split(self, hands: List[PlayerHand], hand_to_split: PlayerHand) -> bool:
        """ If two cards are the same value, split them into two hands """
        within_max_num_hands = len(hands) == 1
        if within_max_num_hands and self.can_split(hand_to_split):
            split_card = hand_to_split.split()
            new_hand = PlayerHand()
            new_hand.add_card(split_card)
            hands.append(new_hand)
            self.update_hand_value(hand_to_split)
            self.update_hand_value(new_hand)
            return True

    def can_split(self, hand: PlayerHand) -> bool:
        cards = hand.get_cards()
        two_cards = len(cards) == 2
        first_card = cards[0]
        second_card = cards[1]
        matching_rank = first_card['rank'] is second_card['rank']
        matching_values = self.get_value(first_card) == self.get_value(second_card)
        return (matching_rank or matching_values) and two_cards

    def is_ten_value(self, card) -> bool:
        rank = card['rank']
        if rank in self.values:
            is_ten = self.values[rank] == 10
        else:
            is_ten = False
        return is_ten

    @staticmethod
    def is_ace(card) -> bool:
        rank = card['rank']
        return rank is 'A'

    def resolve_aces(self, sum_values: int, cards: List[dict]) -> int:
        # Aces always add 1. Then, check if they can add 10 to make the full 11.

        aces = self.get_aces(cards)
        num_aces = len(aces)
        sum_values += num_aces

        for ace in aces:
            is_eleven_bust = (sum_values + 10) > 21
            if not is_eleven_bust:
                sum_values += 10

        return sum_values

    def get_aces(self, cards: List[dict]):
        return list(filter(self.is_ace, cards))

    def draw_card(self) -> dict:
        suit = roll(self.suits)
        rank = roll(self.deck[suit])
        self.deck[suit].remove(rank)
        card = {'rank': rank, 'suit': suit}
        return card

    def _get_hand_value(self, hand: Hand) -> int:
        cards = hand.get_cards()
        sum_values = sum([self.get_value(card) for card in cards])
        hand_value = self.resolve_aces(sum_values, cards)
        return hand_value

    def get_value(self, card) -> int:
        # Aces return a value of 0 and are handled elsewhere
        rank = card['rank']
        if rank in self.values:
            return self.values[rank]
        else:
            return 0

    def is_blackjack(self, hand) -> bool:
        has_ace = False
        has_ten = False
        cards = hand.get_cards()
        two_cards_in_hand = len(cards) == 2
        for card in cards:
            if self.is_ace(card):
                has_ace = True
            elif self.is_ten_value(card):
                has_ten = True
        return two_cards_in_hand and has_ace and has_ten

    def update_hand_value(self, hand):
        value = self._get_hand_value(hand)
        hand.set_value(value)
