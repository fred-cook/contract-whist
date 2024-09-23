import logging

from contract_whist.cards import Card
from contract_whist.trick import Trick
from contract_whist.hand import Hand
from contract_whist.players import Player


class HeuristicPlayer(Player):
    """
    The Heuristic player attempts to play with some tactics,
    using an approximate scoring system for hands and trying
    to win tricks until the contract is made, then throwing
    away as best as possible after.

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
        """
        Round the hand evaluation to a best guess of a
        contract.
        """
        score = self.evaluate_hand(self.hand)
        if round(score) in options:
            bid = round(score)
        elif round(score) > max(options):
            bid = max(options)
        else:
            options = list(options)
            diffs = [abs(score - option) for option in options]
            bid = options[diffs.index(min(diffs))]
        self.contract = bid
        return bid

    def play_card(self, trick: Trick) -> Card:
        """
        play_card follows some basic logic:
        - If the current trick total is the contract try not
          to win any more cards:
           - if leading lead a low card
           - if following lay the highest possible losing card
           - if there is no losing card play the lowest winning card
        - If the current trick total is below or above the contract
          try and win the trick.
           - if leading lay a high card
           - if following suit and can currently win lay that card
           - if the trick is unwinnable throw away a low card
        """
        playable = self.hand.playable(trick)
        if len(playable) == 1:
            logging.debug(f"{self.name} has no choice: {playable[0]} from {self.hand.cards}")
            card = playable.pop()
        elif self.trick_count == self.contract:  # try and throw away cards
            if len(trick) == 0:  # playing first
                card = self.min_face_card(playable)
                logging.debug(f"{self.name} trying to lose with {card} from {self.hand.cards}")
            else:
                card = self.max_losing_card(playable, trick)
                logging.debug(
                    f"{self.name} playing highest losing card from {self.hand.cards}: {card}"
                )
        else:  # try and win it
            if len(trick) == 0:  # playing first
                card = self.max_face_card(playable)
                logging.debug(f"{self.name} trying to win with {card} from {self.hand.cards}")
            elif (card := self.can_win(playable, trick)) is not None:
                logging.debug(f"{self.name} trying to win from {self.hand.cards} with {card}")
            else:
                card = self.min_face_card(playable)
                logging.debug(
                    f"{self.name} can't win, throwing away {card} for {self.hand.cards}"
                )
        return self.hand.play_card(card)

    def max_face_card(self, cards: list[Card]) -> Card:
        # Sort by value to avoid Card's built in trump comparison
        return sorted(cards, key=lambda card: card.value, reverse=True)[0]

    def min_face_card(self, cards: list[Card]) -> Card:
        # Sort by value to avoid Card's built in trump comparison
        return sorted(cards, key=lambda card: card.value)[0]

    def can_win(self, playable_cards: list[Card], trick: Trick) -> Card | None:
        max_card = sorted(playable_cards)[-1]
        if all(card < max_card for card in trick.cards):
            return max_card

    def max_losing_card(self, playable_cards: list[Card], trick: Trick) -> Card:
        """
        Sort the cards by value, highest trump at the end, non-trumps
        sorted by face value. Loop backwards through them until a
        losing card is found, and play that one.

        If no losing card is found play the lowest winning card.
        """
        # reverse so highest card is first
        playable_cards = self.hand.sort_by_value(playable_cards)[::-1]
        for playable_card in playable_cards:
            if trick.winning_card(trick.cards + [playable_card]) is not playable_card:
                return playable_card
        # Can't lose this trick, try and win more, win with lowest possible
        return playable_cards[-1]

    def evaluate_hand(self, hand: Hand) -> float:
        """
        A rough heuristic for evaluating hand strengths
        """
        score = 0.0
        for card in hand.cards:
            if card.suit == card.TRUMP:
                score += card.value * self.trump_multiplier
            else:
                if card.value > self.card_cutoff:
                    score += self.card_multiplier * card.value
        return score / 10
