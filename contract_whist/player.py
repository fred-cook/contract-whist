from os import environ

from contract_whist.deck import Card
from contract_whist.hand import Hand

if environ["TYPE_CHECKING"]:
    from contract_whist.game import Trick

class Player:
    def __init__(self, name: str):
        self.name: str = name
        self.points: int = 0

        self.hand: Hand | None = None

    def make_bid(self, options: set[int]) -> int:
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
        print(f"{self.name} choose from: played so far: {list(trick.cards.values())}")
        for i, card in enumerate(self.hand.cards):
            print(f"{i:2d}" if playable[i] else "  ", f" | {card}")
        index = -1
        while index not in set(i for i, available in enumerate(playable) if available):
            try:
                index = int(input("choose index: "))
            except Exception:
                print("invalid")
        return self.hand.pop(index)

    def __repr__(self):
        return self.name
