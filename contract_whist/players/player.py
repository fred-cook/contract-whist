from abc import ABC, abstractmethod

from contract_whist.cards import Card
from contract_whist.hand import Hand
from contract_whist.trick import Trick


class Player(ABC):
    """
    Base class for a player.

    Contains helper methods for keeping track of the
    player's contract, tricks and total score.

    Inheritors must define a method to bid on a hand
    and to play cards.
    """
    def __init__(self, name: str):
        self.name: str = name
        self.points: int = 0

        self.hand: Hand | None = None
        self.contract: int | None = None  # number of tricks to make
        self.trick_count = 0  # current number of tricks in the round
        self.cards_seen: list[Card] = []

    def __repr__(self):
        return self.name

    def update_trick_result(self, trick: Trick) -> None:
        """
        Once all the cards have been seen update the
        player's trick count and cards seen
        """
        if trick.winner is self:
            self.trick_count += 1
        self.cards_seen += trick.cards

    def round_reset(self) -> None:
        """
        At the end of each round reset the round specific
        attributes
        """
        self.contract = None
        self.trick_count = 0
        self.cards_seen = []

    def update_score(self, score: int) -> None:
        """
        At the end of each round update the player's points
        """
        self.round_reset()
        self.points += score

    @abstractmethod
    def make_bid(self, options: set[int]) -> int: ...

    @abstractmethod
    def play_card(self, trick: Trick) -> Card: ...
