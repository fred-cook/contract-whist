from __future__ import annotations


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from contract_whist.game import Trick, Card, Hand

from contract_whist.players import Player


class HeuristicPlayer(Player):
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
        if sum(playable) == 1:
            return self.hand.pop(playable.index(1))
        elif self.trick_count == self.contract:  # try and throw away cards
            if len(trick) == 0:  # playing first
                return self.hand.pop(self.min_face_card_index(self.hand.cards))
            else:
                return self.hand.pop(
                    self.hand.cards.index(
                        self.max_losing_card(
                            [
                                self.hand.cards[i]
                                for i, can_play in enumerate(playable)
                                if can_play
                            ]
                        ),
                        trick,
                    )
                )
        else:  # try and win it
            if len(trick) == 0:  # playing first
                return self.hand.pop(self.max_face_card_index(self.hand))
            elif (
                card := self.can_win(
                    [
                        self.hand.cards[i]
                        for i, can_play in enumerate(playable)
                        if can_play
                    ],
                    trick,
                )
            ) is not None:
                return self.hand.pop(self.hand.cards.index(card))
            else:
                return self.hand.pop(
                    self.min_face_card_index(
                        [
                            self.hand.cards[i]
                            for i, can_play in enumerate(playable)
                            if can_play
                        ]
                    )
                )

    def max_face_card_index(self, hand: Hand) -> int:
        values = [card.value for card in hand.cards]
        return values.index(max(values))

    def min_face_card_index(self, cards: list[Card]) -> int:
        values = [card.value for card in cards]
        return values.index(min(values))

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
        print(hand)
        score = 0.0
        for card in hand.cards:
            if card.suit == card.TRUMP:
                score += card.value * self.trump_multiplier
            else:
                if card.value > self.card_cutoff:
                    score += self.card_multiplier * card.value
        return score / 10
