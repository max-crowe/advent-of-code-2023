#!/usr/bin/env python
import sys
from argparse import ArgumentParser
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from day4.card import set_winnings
from day4.parser import get_cards_from_input

parser = ArgumentParser()
parser.add_argument(
    "data",
    type=open,
)
parser.add_argument(
    "-m", "--mode",
    choices=["total-value", "count-winnings"]
)

if __name__ == "__main__":
    args = parser.parse_args()
    cards = list(get_cards_from_input(args.data))
    if args.mode == "total-value":
        print(sum(card.value for card in cards))
    else:
        set_winnings(cards)
        print(sum(len(card) for card in cards))
