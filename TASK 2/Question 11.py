import random

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return f"{self.rank} of {self.suit}"

    def is_consecutive(self, other):
        ranks = "23456789TJQKA"
        return abs(ranks.index(self.rank) - ranks.index(other.rank)) == 1

    def is_same_suit(self, other):
        return self.suit == other.suit

class Deck:
    def __init__(self):
        ranks = "23456789TJQKA"
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        self.cards = [Card(rank, suit) for rank in ranks for suit in suits]

    def shuffle(self):
        random.shuffle(self.cards)

    def is_pair(self, cards):
        if len(cards) != 2:
            return False

        card1, card2 = cards
        return (
            (card1.is_consecutive(card2) or (card1.rank == "A" and card2.rank == "2") or (card1.rank == "2" and card2.rank == "A"))
            and card1.is_same_suit(card2)
        )


deck = Deck()
deck.shuffle()
hand = [deck.cards[0], deck.cards[1]]  
print(f"Hand: {hand[0]}, {hand[1]}")
is_pair = deck.is_pair(hand)
if is_pair:
    print("It's a pair!")
else:
    print("Not a pair.")
