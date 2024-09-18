import numpy as np

from contract_whist.cards import Card, Deck, SUITS
from contract_whist.hand import Hand
from contract_whist.trick import Trick
from contract_whist.players import Player


class NNPlayer(Player):
    DECK = Deck()  # used for 1 hot encoding methods

    def __init__(self, name: str):
        self.trick_count_vector = np.zeros(4)

        super().__init__(name)

    def generate_vector(self, trick: Trick):
        """
        The state vector is:
        + Current hand    |  [52]
        + All cards seen  |  [52]
        + Current trick   |  [52]
        + Tricks won      |  [04]
        + Trump           |  [04]
        ------------------+------
                          |  168
        """
        current_hand_vector = self.get_card_vector(self.hand.cards)
        all_cards_seen_vector = self.get_card_vector(self.cards_seen)
        current_trick_vector = self.get_card_vector(trick.cards, ordered=True)

    def get_card_vector(self, cards: list[Card], ordered: bool = False) -> np.ndarray:
        """
        Return a 1 hot encoded vector of the list of cards

        If ordered is true then the first card is given twice the weight
        """
        vector = np.zeros(len(self.DECK))
        for i, card in enumerate(cards):
            vector[card.index] = 2.0 if ordered and i == 0 else 1.0
        return vector

    def update_trick_result(self, trick: Trick) -> None:
        self.trick_count_vector = np.array(
            [
                num_tricks
                for player, num_tricks in sorted(
                    zip(trick.players, trick.cards), key=lambda x: x[0].name
                )
            ]
        )
        return super().update_trick_result(trick)

    def make_bid(self, options: set[int]) -> int: ...
