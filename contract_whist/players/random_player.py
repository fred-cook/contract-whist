from random import choice

from contract_whist.players.player import Player

from contract_whist.cards import Card
from contract_whist.trick import Trick


class RandomPlayer(Player):
    """
    Randomly choose from the available options
    """

    def make_bid(self, options: set[int]) -> int:
        return choice(list(options))

    def play_card(self, trick: Trick) -> Card:
        playable = self.hand.playable(trick)
        return self.hand.play_card(choice(playable))
