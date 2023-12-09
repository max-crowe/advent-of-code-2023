from contextlib import ExitStack
from io import TextIOBase

from .cards import Card, FaceCard, Hand, HandCollection, jokers_wild


def get_hand_collection_from_input(input_data: TextIOBase, make_jokers_wild: bool = False) -> HandCollection:
    hands: list[Hand] = []
    with ExitStack() as stack:
        if make_jokers_wild:
            stack.enter_context(jokers_wild())
        for line in input_data:
            cards_str, _, bid = line.strip().partition(" ")
            hands.append(
                Hand(
                    int(bid),
                    *tuple(
                        Card(int(val) if val.isdigit() else FaceCard[val]) for val in cards_str
                    )
                )
            )
        return HandCollection(*tuple(hands))
