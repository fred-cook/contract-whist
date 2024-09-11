from abc import ABC, abstractmethod


class Player(ABC):
    def __init__(self, name: str):
        self.name: str = name
        self.points: int = 0

        self.hand: "Hand" | None = None

    @abstractmethod
    def make_bid(self, options: set[int]) -> int: ...

    @abstractmethod
    def play_card(self, trick: "Trick") -> "Card": ...

    def __repr__(self):
        return self.name
