from contextlib import contextmanager
from enum import IntEnum, auto
from functools import cached_property, total_ordering


class State:
    def __init__(self):
        self.JOKERS_WILD = False


@contextmanager
def jokers_wild():
    try:
        _state.JOKERS_WILD = True
        yield
    finally:
        _state.JOKERS_WILD = False


class FaceCard(IntEnum):
    T = 10
    J = 11
    Q = 12
    K = 13
    A = 14


class HandType(IntEnum):
    HIGH_CARD = auto()
    ONE_PAIR = auto()
    TWO_PAIR = auto()
    THREE_OF_A_KIND = auto()
    FULL_HOUSE = auto()
    FOUR_OF_A_KIND = auto()
    FIVE_OF_A_KIND = auto()



@total_ordering
class Card:
    def __init__(self, value: int | FaceCard):
        if value < 2 or value > FaceCard.A:
            raise ValueError("Card value out of bounds")
        self.value = value

    def __eq__(self, other: "Card") -> bool:
        return int(self) == int(other)

    def __lt__(self, other: "Card") -> bool:
        return int(self) < int(other)

    def __int__(self) -> int:
        if self.value is FaceCard.J and _state.JOKERS_WILD:
            return 1
        return int(self.value)


@total_ordering
class Hand:
    def __init__(self, bid: int, *cards: Card):
        if len(cards) != 5:
            raise ValueError("Hands must have exactly five cards")
        self.bid = bid
        self.cards = cards
        cards_by_value: dict[int, list[Card]] = {}
        wild_cards: list[Card] = []
        for card in cards:
            if card.value is FaceCard.J and _state.JOKERS_WILD:
                wild_cards.append(card)
                continue
            try:
                cards_by_value[int(card)].append(card)
            except KeyError:
                cards_by_value[int(card)] = [card]
        self.cards_by_value = list(cards_by_value.values())
        self.cards_by_value.sort(key=lambda card_list: len(card_list), reverse=True)
        if not self.cards_by_value:
            assert len(wild_cards) == 5
            self.cards_by_value.append([])
        self.cards_by_value[0].extend(wild_cards)

    def __eq__(self, other: "Hand") -> bool:
        return self.cards == other.cards

    def __lt__(self, other: "Hand") -> bool:
        if self.type != other.type:
            return self.type < other.type
        for i in range(len(self.cards)):
            if self.cards[i] != other.cards[i]:
                return self.cards[i] < other.cards[i]
        return False

    @cached_property
    def type(self) -> HandType:
        if len(self.cards_by_value[0]) == 5:
            return HandType.FIVE_OF_A_KIND
        if len(self.cards_by_value[0]) == 4:
            return HandType.FOUR_OF_A_KIND
        if len(self.cards_by_value[0]) == 3:
            if len(self.cards_by_value[1]) == 2:
                return HandType.FULL_HOUSE
            return HandType.THREE_OF_A_KIND
        if len(self.cards_by_value[0]) == 2:
            if len(self.cards_by_value[1]) == 2:
                return HandType.TWO_PAIR
            return HandType.ONE_PAIR
        assert len(self.cards_by_value) == 5
        return HandType.HIGH_CARD


class HandCollection:
    def __init__(self, *hands: Hand):
        self.hands = list(hands)
        self.hands.sort()

    @cached_property
    def values(self) -> list[int]:
        return [i * hand.bid for i, hand in enumerate(self.hands, 1)]


_state = State()
