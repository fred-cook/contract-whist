from functools import reduce
from operator import add
from collections import defaultdict
from typing import Iterator

from contract_whist.cards import Card
from contract_whist.trick import Trick


class Hand:
    def __init__(self, cards: list[Card]):
        self.cards = sorted(self.sort_hand(cards))
        self.total = len(cards)

    def __len__(self) -> int:
        return len(self.cards)

    def __getitem__(self, key: int) -> Card:
        return self.cards[key]

    def __iter__(self) -> Iterator:
        return iter(self.cards)

    def __str__(self):
        return "\n".join(["-" * 15] + list((map(str, self.cards))) + ["-" * 15])

    def __repr__(self):
        return str(self)
    
    @property
    def trick_proportion(self) -> float:
        return (self.total - len(self)) / self.total

    @staticmethod
    def sort_hand(cards: list[Card]) -> list[Card]:
        """
        This method sorts the cards by suit, and by order
        in that suit
        """
        suits = defaultdict(list)
        for card in cards:
            suits[card.suit].append(card)
        return reduce(add, map(sorted, suits.values()))

    @staticmethod
    def sort_by_value(cards: list[Card]) -> list[Card]:
        """
        Cards are sorted by value for non-trump cards
        independent of suit, then trumps by value.
        """
        return sorted(
            [card for card in cards if card.suit != card.TRUMP],
            key=lambda card: card.value,
        ) + sorted([card for card in cards if card.suit == card.TRUMP])

    @property
    def suits(self) -> set[str]:
        return set(card.suit for card in self.cards)

    def playable(self, trick: Trick) -> list[Card]:
        """
        Return the list of playable cards given that the
        player MUST follow suit if they can
        """
        if trick.lead_suit in self.suits:
            # must follow suit, if leading then lead_suit is None
            return [card for card in self.cards if card.suit == trick.lead_suit]
        else:
            return self.cards[:]  # copy of self.cards

    def pop(self, index: int) -> Card:
        return self.cards.pop(index)

    def play_card(self, card: Card) -> Card:
        """
        Remove the selected card from the hand and return it

        raises ValueError if card not in hand
        """
        return self.cards.pop(self.cards.index(card))
