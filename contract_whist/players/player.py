from __future__ import annotations

from abc import ABC, abstractmethod

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from contract_whist.game import Trick, Card, Hand


class Player(ABC):
    def __init__(self, name: str):
        self.name: str = name
        self.points: int = 0

        self.hand: Hand | None = None
        self.contract: int | None = None  # number of tricks to make
        self.trick_count = 0  # current number of tricks in the round
        self.cards_seen: list[Card] = []

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

    def __repr__(self):
        return self.name
