import numpy as np


from contract_whist.game import Game
from contract_whist.players import DataPlayer


class HarvestData(Game):
    def __init__(self, players: list[DataPlayer]):
        self.input_vectors: list[np.ndarray] = []
        self.output_vectors: list[np.ndarray] = []

        super().__init__(players)

    def play_round(self, num_tricks: int, trump: str | None) -> dict[DataPlayer, int]:

        round_result = super().play_round(num_tricks, trump)

        # extract and process the vectors
        for player in self.players:
            indices = player.play_indices
            # convert the played indices into a 1 hot encoded
            # vector of the card that was played, with 1.0 if
            # the contract was made else -1.0
            played_vectors = np.zeros((len(indices), len(self.DECK)))
            result = 1.0 if player.contract == player.trick_count else -1.0
            played_vectors[np.arange(len(indices)), indices] = result

            self.input_vectors.append(np.array(player.state_vectors))
            self.output_vectors.append(played_vectors)

        return round_result


players = [DataPlayer(name, 1.05, 0.35, 6) for name in ("Fred", "Murray", "Sam", "Tim")]
data_game = HarvestData(players)
data_game.play_game([5, 5, 5])
