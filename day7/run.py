#!/usr/bin/env python

import sys
from argparse import ArgumentParser
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from day7.parser import get_hand_collection_from_input


parser = ArgumentParser()
parser.add_argument(
    "data",
    type=open,
)
parser.add_argument(
    "--jokers-wild",
    action="store_true"
)

if __name__ == "__main__":
    args = parser.parse_args()
    collection = get_hand_collection_from_input(args.data, args.jokers_wild)
    print(sum(collection.values))
