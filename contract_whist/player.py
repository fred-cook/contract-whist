from collections import defaultdict
from functools import reduce
from operator import add

from deck import Card

# from trick import Trick


class Hand:
    def __init__(self, cards: list[Card]):
        self.cards = self.sort_hand(cards)

    def __len__(self) -> int:
        return len(self.cards)

    @staticmethod
    def sort_hand(cards: list[Card]) -> list[Card]:
        suits = defaultdict(list)
        for card in cards:
            suits[card.suit].append(card)
        return reduce(add, map(sorted, suits.values()))

    @property
    def suits(self):
        return set(card.suit for card in self.cards)

    def playable(self, trick: "Trick") -> list[int]:
        if len(trick) == 0:  # leading
            return [1] * len(self)
        elif trick.lead_suit in self.suits:
            return [1 if card.suit == trick.lead_suit else 0 for card in self.cards]
        else:
            return [1] * len(self)

    def pop(self, index: int) -> Card:
        return self.cards.pop(index)

    def __str__(self):
        return "\n".join(["-" * 15] + list((map(str, self.cards))) + ["-" * 15])


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

    def play_card(self, trick: "Trick") -> Card:
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
