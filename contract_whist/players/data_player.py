import numpy as np

from contract_whist.cards import Card, SUITS
from contract_whist.trick import Trick
from contract_whist.players import HeuristicPlayer


class DataPlayer(HeuristicPlayer):

    def __init__(
        self,
        name: str,
        trump_multiplier: float,
        card_multiplier: float,
        card_cutoff: int,
    ):
        self.state_vectors: list[list[int | float]] = []
        self.play_indices: list[int] = []

        super().__init__(name, trump_multiplier, card_multiplier, card_cutoff)


    def generate_vector(self, trick: Trick) -> list[int | float]:
        """
        The state vector is:
        + Current hand    |  [52]
        + All cards seen  |  [52]
        + Current trick   |  [52]
        + Contract        |  [01]
        + Tricks won      |  [01]
        + Trick fraction  |  [01]
        + Trump           |  [04]
        ------------------+------
                          |  163
        """
        return (
            self.get_card_vector(self.hand.cards)
            + self.get_card_vector(self.cards_seen)
            + self.get_card_vector(trick.cards, ordered=True)
            + [self.contract, self.trick_count, self.hand.trick_fraction]
            + self.get_trump_vector()
        )

    def get_card_vector(self, cards: list[Card], ordered: bool = False) -> list[int]:
        """
        Return a ~1 hot encoded vector of the list of cards

        If ordered is true then the first card is given twice the weight
        """
        vector = len(self.DECK) * [0]
        for i, card in enumerate(cards):
            vector[card.index] = 2 if ordered and i == 0 else 1
        return vector
    
    def get_trump_vector(self) -> list[int]:
        """
        One hot encoding for what is trumps, all
        0 if no trumps.
        """
        return np.ndarray([1 if suit == Card.TRUMP else 0
                           for suit in SUITS])
    
    def round_reset(self) -> None:
        self.state_vectors = []
        self.play_indices = []
        return super().round_reset()

    def play_card(self, trick: Trick) -> Card:
        self.state_vectors.append(self.generate_vector(trick))
        card = super().play_card(trick)
        self.play_indices.append(card.index)
        return card
