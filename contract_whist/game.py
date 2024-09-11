from itertools import cycle
from enum import IntEnum
from random import shuffle
from collections import defaultdict
from functools import reduce
from operator import add

from contract_whist.players import Player, HumanPlayer, RandomPlayer


Values = IntEnum(
    "Values", list(map(str, range(2, 11))) + ["jack", "queen", "king", "ace"]
)
SUITS = ("club", "diamond", "heart", "spade")


class Card:
    TRUMP: str | None = None

    def __init__(self, suit: str, value: IntEnum):
        self.suit = suit
        self.value = value

    def __repr__(self):
        return f"{self.value.name} of {self.suit}s"

    def __lt__(self, other):
        if other.suit != self.suit and self.suit == self.TRUMP:
            return False
        elif other.suit != self.suit and other.suit == self.TRUMP:
            return True
        elif other.suit != self.suit:
            return False  # because order of play matters
        else:
            return self.value < other.value

    def __gt__(self, other):
        return not (self.__lt__(other))

    @classmethod
    def set_trump(cls, suit: str | None) -> None:
        if suit in SUITS + (None,):
            cls.TRUMP = suit
        else:
            raise ValueError(f"suit must be in {SUITS + (None,)} not {suit}")


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
        return [
            player for player, _ in sorted(self.cards.items(), key=lambda pair: pair[1])
        ].pop()


class Hand:
    def __init__(self, cards: list[Card]):
        self.cards = self.sort_hand(cards)

    def __len__(self) -> int:
        return len(self.cards)

    @staticmethod
    def sort_hand(cards: list[Card]) -> list[Card]:
        suits = defaultdict(list)
        for card in cards:
            suits[card.suit].append(card)
        return reduce(add, map(sorted, suits.values()))

    @property
    def suits(self):
        return set(card.suit for card in self.cards)

    def playable(self, trick: Trick) -> list[int]:
        if len(trick) == 0:
            # leading
            return [1] * len(self)
        elif trick.lead_suit in self.suits:
            # must follow suit
            return [1 if card.suit == trick.lead_suit else 0 for card in self.cards]
        else:
            # can't follow suit
            return [1] * len(self)

    def pop(self, index: int) -> Card:
        return self.cards.pop(index)

    def __str__(self):
        return "\n".join(["-" * 15] + list((map(str, self.cards))) + ["-" * 15])


class Deck:
    def __init__(self):
        self.cards = [Card(suit, value) for suit in SUITS for value in Values]

    def __getitem__(self, value):
        return self.cards[value]

    def shuffle_and_deal(self, num_cards: int, num_players: int) -> list[Hand]:
        total_cards = num_cards * num_players
        if num_cards > 0 and num_players > 0 and total_cards < len(self.cards):
            shuffle(self.cards)  # in place
            return [
                Hand([self.cards[i] for i in range(j, total_cards, num_players)])
                for j in range(num_players)
            ]

    @staticmethod
    def set_trump(suit: str | None) -> None:
        Card.set_trump(suit)


class Game:
    CONTRACT_BONUS: int = 10

    SUIT_ORDER = cycle(SUITS + (None,))
    DECK: Deck = Deck()

    def __init__(self, players: list[Player]):
        self.players = players

        self.bids: dict[str, int] | None = None
        self.rounds = list(range(7, 0, -2)) + list(range(2, 8, 2))

    @property
    def num_players(self) -> int:
        return len(self.players)

    def get_bids(self, hands: list[Hand]) -> dict[str, int]:
        """
        Get the bids in current playing order, with
        the exception that the sum of the bids can't
        match the total tricks available.
        """
        options = set(range(len(hands[0]) + 1))
        bids = {}
        for player, hand in zip(players, hands):
            print(f"{player.name} to bid.")
            player.hand = hand
            if player is players[-1]:  # dealer
                if (forbidden := len(hands[0]) - sum(bids.values())) >= 0:
                    options.remove(forbidden)
            bids[player] = player.make_bid(options)
        return bids

    def play_round(self, num_tricks: int, trump: str | None) -> dict[Player, int]:
        """
        Play proceeds as follows:
            - Deal a hand to each player
            - Collect the bids
            - Lay cards
            - total scores
        """
        self.DECK.set_trump(trump)
        hands = self.DECK.shuffle_and_deal(
            num_cards=num_tricks, num_players=self.num_players
        )
        bids = self.get_bids(hands)
        for player, bid in bids.items():
            print(f"{player.name:<20s} | {bid:2d}")

        tricks: dict[Player, int] = {player: 0 for player in self.players}

        leader_index = 0
        for trick_number in range(num_tricks):
            print(f"trick {trick_number + 1}:")
            trick = Trick(trump)
            for player in self.players[leader_index:] + self.players[:leader_index]:
                trick.add_card(player, player.play_card(trick))

            winner = trick.resolve()
            leader_index = self.players.index(winner)
            tricks[winner] += 1

        return {
            player: score + self.CONTRACT_BONUS if score == bids[player] else score
            for player, score in tricks.items()
        }

    def play_game(self) -> dict[Player, int]:
        """
        Play the specified number of rounds, adding the scores
        """
        scores = {player: 0 for player in self.players}
        hands = [4, 2, 1, 3, 5]
        for i, hand in enumerate(hands):
            trump = next(self.SUIT_ORDER)
            print(f"Round {i + 1}: {hand} cards, {trump}s are trumps")
            print(f"{self.players[-1].name} is dealing")
            round_result = self.play_round(num_tricks=hand, trump=trump)
            for player, score in round_result.items():
                print(f"{player.name:10s} | {score:2d}")
                scores[player] += score
            self.players.append(self.players.pop(0))  # next dealer
        print("Final scores:")
        for player, score in scores.items():
            print(f"{player.name:10s} | {score:3d}")

    @staticmethod
    def new_leader(winner: Player, players: list[Player]) -> list[Player]:
        index = players.index(winner)
        return players[index:] + players[:index]


if __name__ == "__main__":
    players = [HumanPlayer("Ferd")] + [
        RandomPlayer(name) for name in ["Gurple", "Snerp", "Morsh"]
    ]
    game = Game(players)

    x = game.play_game()
