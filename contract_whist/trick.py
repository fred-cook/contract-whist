from __future__ import annotations
from typing import TYPE_CHECKING

import logging
logging.basicConfig(level=logging.CRITICAL)

from contract_whist.cards import Card
if TYPE_CHECKING:
    from contract_whist.players import Player

class Trick:
    """
    A trick will eventually consist of a card for
    each player once they have all laid.
    """
    def __init__(self):
        self.cards: list[Card] = []
        self.players: list[Player] = []
        self.lead_suit: str | None = None

        self.winner: Player | None = None

    def __len__(self):
        return len(self.cards)
    
    def __iter__(self):
        return iter(self.cards)

    def add_card(self, player: Player, card: Card) -> None:
        """
        Add a card to the trick. Need to know
        the player and the card. If it's the first
        card it sets the lead suit.
        """
        if self.lead_suit is None:
            self.lead_suit = card.suit
        self.cards.append(card)
        self.players.append(player)

    def resolve(self) -> Player:
        """
        Once all the cards have been laid work out who won.

        Store winning player as attr so this trick can be
        passed to all players to look at the cards played
        and resulting winner.
        """
        for player, card in zip(self.players, self.cards):
            logging.info(f"{player.name:10s} | {card}")
        winning_card = self.winning_card(self.cards)
        self.winner = self.players[self.cards.index(winning_card)]
        logging.info(f"{self.winner.name} wins with the {winning_card}")
        return self.winner

    @staticmethod
    def winning_card(cards: list[Card]) -> Card:
        """
        Work out the winning card, note that laying
        order is important.
        """
        winning_card, *rest = cards
        for card in rest:
            if winning_card < card:
                winning_card = card
        return winning_card