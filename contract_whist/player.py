from deck import Card

# from trick import Trick


class Hand:
    def __init__(self, cards: list[Card]):
        self.cards = cards

    def __len__(self) -> int:
        return len(self.cards)

    @property
    def suits(self):
        return set(card.suit for card in self.cards)

    def playable(self, trick: "Trick") -> list[Card]:
        if len(trick) == 0:  # leading
            return self.cards
        elif trick.lead_suit in self.suits:
            return [card for card in self.cards if card.suit == trick.lead_suit]
        else:
            return self.cards

    def pop(self, index: int) -> Card:
        return self.cards.pop(index)

    def __str__(self):
        return "\n".join(["-" * 15] + list((map(str, self.cards))) + ["-" * 15])


class Player:
    def __init__(self, name: str):
        self.name: str = name
        self.points: int = 0

        self.hand: Hand | None = None

    def make_bid(self, options: set[int]) -> int:
        bid = -1
        print(self.hand)
        while bid not in options:
            try:
                bid = int(input(f"Choose your bid from {options}: "))
            except Exception:
                print("invalid")
        return bid

    def play_card(self, trick: "Trick") -> Card:
        playable = self.hand.playable(trick)
        print(f"{self.name} choose from: played so far: {list(trick.cards.values())}")
        for i, card in enumerate(playable):
            print(f"{i:2d}: {card}")
        index = -1
        while not (0 <= index < len(self.hand)):
            try:
                index = int(input("choose index: "))
            except Exception:
                print("invalid")
        return self.hand.pop(self.hand.cards.index(playable[index]))

    def __repr__(self):
        return self.name
