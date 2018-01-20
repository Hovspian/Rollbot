from Blackjack.hand import Hand
from Core.constants import DOUBLE_SPACE, SPACE


class RenderCard:

    """
    Cards have a [ <rank> <suit> ] format.
    Eg: [ A :spade: ]
    """

    def __init__(self):
        pass

    def render_hand(self, hand: Hand) -> str:
        cards = []
        for card in hand._cards:
            rendered_card = self.render_card(card)
            cards.append(rendered_card)
        return DOUBLE_SPACE.join(cards)

    @staticmethod
    def render_card(card: dict):
        return SPACE.join(["[", card['rank'], card['suit'], "]"])