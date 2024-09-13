from contract_whist.players.player import Player

from contract_whist.trick import Trick
from contract_whist.cards import Card


class HumanPlayer(Player):
    """
    Waits for input by human for bidding and playing
    cards.
    """

    def make_bid(self, options: set[int]) -> int:
        """
        Request the player to enter a bid value
        """
        bid = -1
        print(self.hand)
        while bid not in options:
            try:
                bid = int(input(f"Choose your bid from {options}: "))
            except Exception:
                print("invalid")
        return bid

    def play_card(self, trick: Trick) -> Card:
        playable = self.hand.playable(trick)
        print(f"{self.name} choose from: played so far: {trick.cards}")
        for i, card in enumerate(self.hand):
            print(f"{i:2d}" if card in playable else "  ", f" | {card}")
        index = -1
        while index not in set(
            i for i, card in enumerate(self.hand) if card in playable
        ):
            try:
                index = int(input("choose index: "))
            except Exception:
                print("invalid")
        return self.hand.pop(index)
