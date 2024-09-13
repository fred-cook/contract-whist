from itertools import cycle

import numpy as np
import matplotlib.pyplot as plt

from contract_whist.players import Player, HumanPlayer, RandomPlayer, HeuristicPlayer

from contract_whist.cards import Deck, SUITS
from contract_whist.hand import Hand
from contract_whist.trick import Trick


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
            player.hand = hand
            if player is players[-1]:  # dealer
                if (forbidden := len(hands[0]) - sum(bids.values())) >= 0:
                    options.remove(forbidden)
            print(f"{player.name} to bid: {(bid := player.make_bid(options))}")
            bids[player] = bid
        return bids

    def play_round(self, num_tricks: int, trump: str | None) -> dict[Player, int]:
        """
        Play proceeds as follows:
            - Deal a hand to each player
            - Collect the bids
            - Lay cards
            - Total scores
        """
        self.DECK.set_trump(trump)
        hands = self.DECK.shuffle_and_deal(
            num_cards=num_tricks, num_players=self.num_players
        )
        bids = self.get_bids([Hand(cards) for cards in hands])
        for player, bid in bids.items():
            print(f"{player.name:<20s} | {bid:2d}")

        tricks: dict[Player, int] = {player: 0 for player in self.players}

        leader_index = 0
        for trick_number in range(num_tricks):
            print(f"trick {trick_number + 1}:")
            trick = Trick()
            for player in self.players[leader_index:] + self.players[:leader_index]:
                trick.add_card(player, player.play_card(trick))

            winner = trick.resolve()
            leader_index = self.players.index(winner)
            tricks[winner] += 1

        return {
            player: score + self.CONTRACT_BONUS if score == bids[player] else score
            for player, score in tricks.items()
        }

    def play_game(self) -> None:
        """
        Play the specified number of rounds, adding the scores
        """
        hands = [12, 10, 8, 6, 4, 2, 1, 3, 5, 7, 9, 11, 13]
        # hands = [4, 2, 1, 3, 5]
        for i, hand in enumerate(hands):
            trump = next(self.SUIT_ORDER)
            trump_message = "no trumps" if trump is None else f"{trump}s are trumps"
            print(f"Round {i + 1}: {hand} cards, {trump_message}")
            print(f"{self.players[-1].name} is dealing")
            round_result = self.play_round(num_tricks=hand, trump=trump)
            for player, score in round_result.items():
                print(f"{player.name:10s} | {score:2d}")
                player.update_score(score)
            self.players.append(self.players.pop(0))  # next dealer
        print("Final scores:")
        for player in self.players:
            print(f"{player.name:10s} | {player.points:3d}")
        return {player.name: player.points for player in players}

    @staticmethod
    def new_leader(winner: Player, players: list[Player]) -> list[Player]:
        index = players.index(winner)
        return players[index:] + players[:index]


players = [HumanPlayer("Fred")] + [
    HeuristicPlayer(name, 1.05, 0.35, 6) for name in ("Joe", "Tim", "Cookie")
]
game = Game(players)
game.play_game()

# if __name__ == "__main__":
#     trump_multipliers = np.linspace(0.95, 1.3, 10)
#     card_multipliers = np.linspace(0.1, 0.5, 10)

#     win_ratios = np.zeros((len(trump_multipliers), len(card_multipliers)))
#     average_score = np.zeros((len(trump_multipliers), len(card_multipliers)))

#     REPEATS = 1000

#     for i, trump_multiplier in enumerate(trump_multipliers):
#         for j, card_multiplier in enumerate(card_multipliers):
#             wins = {name: 0 for name in ["Ferd", "Snerp", "Morsh", "Gurple"]}
#             cumulative = {name: 0 for name in ["Ferd", "Snerp", "Morsh", "Gurple"]}

#             for _ in range(REPEATS):
#                 players = [
#                     HeuristicPlayer("Gurple", trump_multiplier, card_multiplier, 6)
#                 ] + [RandomPlayer(name) for name in ["Ferd", "Snerp", "Morsh"]]
#                 game = Game(players)

#                 result = sorted(
#                     game.play_game().items(), key=lambda x: x[1], reverse=True
#                 )
#                 wins[result[0][0]] += 1
#                 for name, score in result:
#                     cumulative[name] += score
#             win_ratios[i][j] = wins["Gurple"] / sum(wins.values())
#             average_score[i][j] = cumulative["Gurple"] / REPEATS

#     fig, (ax1, ax2) = plt.subplots(1, 2)
#     ax1.imshow(win_ratios)
#     ax1.set_xticks(
#         np.arange(len(card_multipliers)),
#         [f"{val:.2f}" for val in card_multipliers],
#         rotation="vertical",
#     )
#     ax1.set_ylabel("trump multiplier")
#     ax1.set_xlabel("card multiplier")
#     ax1.set_yticks(
#         np.arange(len(trump_multipliers)),
#         [f"{val:.2f}" for val in trump_multipliers],
#     )
#     ax1.set_title("win ratio")
#     ax2.imshow(average_score)
#     ax2.set_ylabel("trump multiplier")
#     ax2.set_xlabel("card multiplier")
#     ax2.set_xticks(
#         np.arange(len(card_multipliers)),
#         [f"{val:.2f}" for val in card_multipliers],
#         rotation="vertical",
#     )
#     ax2.set_yticks(
#         np.arange(len(trump_multipliers)),
#         [f"{val:.2f}" for val in trump_multipliers],
#     )
#     ax2.set_title("Avg score")
#     plt.show()
