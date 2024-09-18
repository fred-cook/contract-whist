import numpy as np

from contract_whist.cards import Card, Deck
from contract_whist.hand import Hand
from contract_whist.trick import Trick
from contract_whist.players import Player


class NNPlayer(Player):
    def generate_vector(self, trick: Trick):
        """
        The state vector is:
        + Current hand    |  [52]
        + All cards seen  |  [52]
        + Current trick   |  [52]
        + Contracts       |  [04]
        + Tricks won      |  [04]
        + Trump           |  [04]
        ------------------+------
                          |  168
        """
        current_hand_vector = np.zeros(52)
        for card in self.hand.cards:
            current_hand_vector[card.index] = 1

    @staticmethod
    def get_card_vector(cards: list[Card]) -> np.ndarray:
        vector = np.zeros(len(Deck()))
        for card in cards:
            vector[card.index] = 1.0
        return vector
