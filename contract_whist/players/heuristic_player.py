from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from contract_whist.game import Trick, Card

from contract_whist.players.player import Player


class HeuristicPlayer(Player):
    def make_bid(self, options: set[int]) -> int: ...

    def play_card(self, trick: Trick) -> Card: ...
