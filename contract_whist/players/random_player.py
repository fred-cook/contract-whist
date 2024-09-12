from random import choice

from contract_whist.players.player import Player

from contract_whist.cards import Card
from contract_whist.trick import Trick





class RandomPlayer(Player):

    def make_bid(self, options: set[int]) -> int:
        return choice(list(options))

    def play_card(self, trick: Trick) -> Card:
        playable = self.hand.playable(trick)
        index = choice([i for i in range(len(self.hand)) if playable[i]])
        return self.hand.pop(index)
