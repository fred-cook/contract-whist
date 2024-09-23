import numpy as np

from contract_whist.cards import Card, Deck, SUITS
from contract_whist.players import Player
from contract_whist.trick import Trick


class GameStateVector:
    DECK = Deck()

    @classmethod
    def generate_vector(cls, player: Player, trick: Trick) -> list[float]:
        """
        The state vector is:
        + Current hand     |  [52]
        + All cards seen   |  [52]
        + Current trick    |  [52]
        + Contract         |  [01]
        + Tricks won       |  [01]
        + Trick proportion |  [01]
        + Total tricks     |  [01]
        + Trump            |  [04]
        -------------------+------
                           |  164
        """
        return (
            cls.get_card_vector(player.hand.cards)
            + cls.get_card_vector(player.cards_seen)
            + cls.get_card_vector(trick.cards, ordered=True)
            + [player.contract, player.trick_count]
            + [player.hand.trick_proportion, player.hand.total]
            + cls.get_trump_vector()
        )
    
    @classmethod
    def get_card_vector(cls, cards: list[Card], ordered: bool = False) -> list[int]:
        """
        Return a ~1 hot encoded vector of the list of cards

        If ordered is true then the first card is given twice the weight
        """
        vector = len(cls.DECK) * [0]
        for i, card in enumerate(cards):
            vector[card.index] = 2 if ordered and i == 0 else 1
        return vector
    
    @classmethod
    def decode_vector(cls, vector: np.ndarray) -> None:
        """
        Print the cards present in the vector
        """
        print("Current hand:")
        cls.print_card_vector(vector[:(index := len(cls.DECK))])
        print("All cards seen:")
        cls.print_card_vector(vector[index: (index := index + len(cls.DECK))])
        print("Current Trick:")
        cls.print_card_vector(vector[index: (index := index + len(cls.DECK))])
        print(f"Contract: {vector[index]}")
        print(f"Trick count: {vector[(index := index + 1)]}")
        print(f"Trick Proportion: {vector[(index := index + 1)]}")
        print(f"Total: {vector[(index := index + 1)]}")
        
        print("No trump" if not any(vector[(index:= index + 1):]) else SUITS[np.argmax(vector[index:])])

    @classmethod
    def print_card_vector(cls, vector: np.ndarray) -> None:
        """
        Expects a 52 long one hot encoded vector
        """
        for card in cls.DECK:
            if vector[card.index]:
                print(card)
    
    @staticmethod
    def get_trump_vector() -> list[int]:
        """
        One hot encoding for what is trumps, all
        0 if no trumps.
        """
        return [1 if suit == Card.TRUMP else 0 for suit in SUITS]