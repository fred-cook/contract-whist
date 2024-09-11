from contract_whist.deck import Card
from contract_whist.player import Player


class Trick:
    def __init__(self, trump: str | None):
        self.trump = trump
        self.cards: dict[Player, Card] = {}
        self.lead_suit: str | None = None

    def __len__(self):
        return len(self.cards)

    def add_card(self, player: Player, card: Card):
        if self.lead_suit is None:
            self.lead_suit = card.suit
        self.cards[player] = card

    def resolve(self) -> Player:
        for player, card in self.cards.items():
            print(f"{player.name:10s} | {card}")
        (winning_player, winning_card), *rest = self.cards.items()
        for player, card in rest:
            if winning_card < card:
                winning_player = player
                winning_card = card
        print(f"{winning_player.name} wins with the {winning_card}")
        return winning_player
