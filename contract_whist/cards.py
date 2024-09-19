from enum import IntEnum
from random import shuffle
from itertools import count

Values = IntEnum(
    "Values", list(map(str, range(2, 11))) + ["jack", "queen", "king", "ace"], start=2
)
SUITS = ("club", "diamond", "heart", "spade")


class Card:
    """
    Each card is a singleton
    """

    TRUMP: str | None = None
    _instances: dict[tuple[str, IntEnum], "Card"] = {}
    _index_counter = count()

    def __new__(cls, suit: str, value: IntEnum):
        if (suit, value) not in cls._instances:
            instance = super().__new__(cls)
            instance.index = next(cls._index_counter)  # for 1 hot encoding
            cls._instances[(suit, value)] = instance
        return cls._instances[(suit, value)]

    def __init__(self, suit: str, value: IntEnum):
        if not hasattr(self, suit):
            self.suit = suit
            self.value = value

    def __repr__(self):
        return f"{self.value.name} of {self.suit}s"

    def __lt__(self, other):
        if other.suit != self.suit and self.suit == self.TRUMP:
            return False
        elif other.suit != self.suit and other.suit == self.TRUMP:
            return True
        elif other.suit != self.suit:
            return False  # because order of play matters
        else:
            return self.value < other.value

    def __gt__(self, other):
        return not (self.__lt__(other))

    @classmethod
    def set_trump(cls, suit: str | None) -> None:
        if suit in SUITS + (None,):
            cls.TRUMP = suit
        else:
            raise ValueError(f"suit must be in {SUITS + (None,)} not {suit}")


class Deck:
    def __init__(self):
        self.cards = [Card(suit, value) for suit in SUITS for value in Values]

    def __getitem__(self, value):
        return self.cards[value]

    def __len__(self):
        return len(self.cards)

    def shuffle_and_deal(self, num_cards: int, num_players: int) -> list[list[Card]]:
        total_cards = num_cards * num_players
        if num_cards > 0 and num_players > 0 and total_cards <= len(self.cards):
            shuffle(self.cards)  # in place
            return [
                [self.cards[i] for i in range(j, total_cards, num_players)]
                for j in range(num_players)
            ]

    @staticmethod
    def set_trump(suit: str | None) -> None:
        Card.set_trump(suit)
