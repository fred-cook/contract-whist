from itertools import cycle

from contract_whist.player import Player, Hand
from contract_whist.deck import Deck, SUITS
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
            print(f"{player.name} to bid.")
            player.hand = Hand(hand)
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

        return {player: score + self.CONTRACT_BONUS if score == bids[player] else score
                for player, score in tricks.items()}
    
    def play_game(self) -> dict[Player, int]:
        """
        Play the specified number of rounds, adding the scores
        """
        scores = {player: 0 for player in self.players}
        hands = [4, 2, 1, 3, 5]
        for i, hand in enumerate(hands):
            trump=next(self.SUIT_ORDER)
            print(f"Round {i + 1}: {hand} cards, {trump}s are trumps")
            print(f"{self.players[-1].name} is dealing")
            round_result = self.play_round(num_tricks=hand,
                                           trump=trump)
            for player, score in round_result.items():
                print(f"{player.name:10s} | {score:2d}")
                scores[player] += score
            self.players.append(self.players.pop(0)) # next dealer
        print("Final scores:")
        for player, score in scores.items():
            print(f"{player.name:10s} | {score:3d}")



    @staticmethod
    def new_leader(winner: Player, players: list[Player]) -> list[Player]:
        index = players.index(winner)
        return players[index:] + players[:index]


if __name__ == "__main__":
    players = [Player(name) for name in ["fred", "chode", "kate", "cam"]]
    game = Game(players)

    x = game.play_game()
