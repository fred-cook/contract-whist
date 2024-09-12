from __future__ import annotations


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from contract_whist.game import Trick, Card, Hand

from contract_whist.players import Player


class HeuristicPlayer(Player):
    """
    By playing the random players the best values were found to be:
    trump_multiplier: 1.05
    card_multiplier: 0.35
    card_cutoff: 6
    """

    def __init__(
        self,
        name: str,
        trump_multiplier: float,
        card_multiplier: float,
        card_cutoff: int,
    ):
        self.trump_multiplier = trump_multiplier
        self.card_multiplier = card_multiplier
        self.card_cutoff = card_cutoff
        super().__init__(name)

    def make_bid(self, options: set[int]) -> int:
        score = self.evaluate_hand(self.hand)
        if round(score) in options:
            return round(score)
        elif round(score) > max(options):
            return max(options)
        else:
            options = list(options)
            diffs = [abs(score - option) for option in options]
            return options[diffs.index(min(diffs))]

    def play_card(self, trick: Trick) -> Card:
        playable = self.hand.playable(trick)
        playable_cards = [card for i, card in enumerate(self.hand.cards) if playable[i]]
        if sum(playable) == 1:
            print(
                f"{self.name} has no choice: {self.hand.cards[playable.index(1)]} from {self.hand.cards}"
            )
            return self.hand.pop(playable.index(1))
        elif self.trick_count == self.contract:  # try and throw away cards
            if len(trick) == 0:  # playing first
                card = self.min_face_card(playable_cards)
                print(f"{self.name} trying to lose with {card} from {self.hand.cards}")
                return self.hand.pop(self.hand.cards.index(card))
            else:
                card = self.max_losing_card(playable_cards, trick)
                print(
                    f"{self.name} playing highest losing card from {self.hand.cards}: {card}"
                )
                return self.hand.pop(self.hand.cards.index(card))
        else:  # try and win it
            if len(trick) == 0:  # playing first
                card = self.max_face_card(playable_cards)
                print(f"{self.name} trying to win with {card} from {self.hand.cards}")
                return self.hand.pop(self.hand.cards.index(card))
            elif (card := self.can_win(playable_cards, trick)) is not None:
                print(f"{self.name} trying to win from {self.hand.cards} with {card}")
                return self.hand.pop(self.hand.cards.index(card))
            else:
                card = self.min_face_card(playable_cards)
                print(
                    f"{self.name} can't win, throwing away {card} for {self.hand.cards}"
                )
                return self.hand.pop(self.hand.cards.index(card))

    def max_face_card(self, cards: list[Card]) -> Card:
        return sorted(cards, key=lambda card: card.value, reverse=True)[0]

    def min_face_card(self, cards: list[Card]) -> Card:
        return sorted(cards, key=lambda card: card.value)[0]

    def can_win(self, playable_cards: list[Card], trick: Trick) -> Card | None:
        max_card = sorted(playable_cards)[-1]
        if all(card < max_card for card in trick.cards):
            return max_card

    def max_losing_card(self, playable_cards: list[Card], trick: Trick) -> Card:
        playable_cards = self.hand.sort_by_value(playable_cards)[::-1]
        for playable_card in playable_cards:
            if trick.winning_card(trick.cards + [playable_card]) is not playable_card:
                return playable_card
        # Can't lost this trick, try and win more, win with lowest possible
        return playable_cards[-1]

    def evaluate_hand(self, hand: Hand) -> float:
        score = 0.0
        for card in hand.cards:
            if card.suit == card.TRUMP:
                score += card.value * self.trump_multiplier
            else:
                if card.value > self.card_cutoff:
                    score += self.card_multiplier * card.value
        return score / 10
