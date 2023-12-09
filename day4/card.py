from dataclasses import dataclass, field
from functools import cached_property


@dataclass
class Card:
    id: int
    winning_numbers: set[int] = field(default_factory=set)
    numbers: set[int] = field(default_factory=set)
    won_cards: list = field(default_factory=list)

    def __len__(self):
        return 1 + sum(len(card) for card in self.won_cards)

    @cached_property
    def match_count(self) -> int:
        return len(self.numbers & self.winning_numbers)

    @cached_property
    def value(self) -> int:
        return 2 ** (self.match_count - 1) if self.match_count else 0


def set_winnings(cards: list[Card]):
    for idx, card in enumerate(cards):
        card.won_cards.extend(cards[idx+1:idx+1+card.match_count])
