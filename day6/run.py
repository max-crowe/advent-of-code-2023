#!/usr/bin/env python

import sys
from argparse import ArgumentParser
from functools import reduce
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from day6.calculator import get_winning_products_count
from day6.parser import get_race_stats_from_input


parser = ArgumentParser()
parser.add_argument(
    "data",
    type=open,
)
parser.add_argument(
    "--strip-spaces",
    action="store_true"
)

if __name__ == "__main__":
    args = parser.parse_args()
    possibilities_list = [
        get_winning_products_count(time, distance)
        for time, distance in get_race_stats_from_input(args.data, args.strip_spaces)
    ]
    if args.strip_spaces:
        assert len(possibilities_list) == 1
        print(possibilities_list[0])
    else:
        print(reduce(lambda a, b: a * b, possibilities_list))
