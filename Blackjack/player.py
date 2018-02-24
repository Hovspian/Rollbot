from Blackjack.hand import PlayerHand


class BlackjackPlayer:

    """
    Represents a user in Blackjack. Players can have multiple hands.
    """

    def __init__(self, user):
        self.user = user
        self._hands = [PlayerHand()]
        self.name = user.display_name
        self.afk = 0

    def split_hand(self):
        if self._can_split():
            split_card = self.get_active_hand().split()
            new_hand = self._add_hand()
            new_hand.add_card(split_card)
            return True

    def get_hands(self):
        return self._hands

    def get_active_hand(self) -> PlayerHand:
        for hand in self._hands:
            if hand.is_active:
                return hand

    def bust_active_hand(self):
        hand = self.get_active_hand()
        self._remove_hand(hand)
        return hand

    def _can_split(self) -> bool:
        hand = self.get_active_hand()
        return len(self._hands) == 1 and hand.can_split()

    def _add_hand(self):
        hand = PlayerHand()
        self._hands.append(hand)
        return hand

    def _remove_hand(self, hand):
        self._hands.remove(hand)