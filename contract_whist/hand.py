from collections import defaultdict
from functools import reduce
from operator import add

from contract_whist.deck import Card
from contract_whist.trick import Trick

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

    def playable(self, trick: Trick) -> list[int]:
        if len(trick) == 0:
            # leading
            return [1] * len(self)
        elif trick.lead_suit in self.suits:
            # must follow suit
            return [1 if card.suit == trick.lead_suit else 0 for card in self.cards]
        else:
            # can't follow suit
            return [1] * len(self)

    def pop(self, index: int) -> Card:
        return self.cards.pop(index)

    def __str__(self):
        return "\n".join(["-" * 15] + list((map(str, self.cards))) + ["-" * 15])