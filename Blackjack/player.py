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

    def add_hand(self):
        self._hands.append(PlayerHand())

    def get_hands(self):
        return self._hands

    def get_active_hand(self) -> PlayerHand:
        for hand in self._hands:
            if hand.is_active:
                return hand

    def bust_current_hand(self):
        hand = self.get_active_hand()
        self._remove_hand(hand)

    def _remove_hand(self, hand):
        self._hands.remove(hand)