#!/usr/bin/env python

import sys
from argparse import ArgumentParser
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from day8.parser import get_directions_and_map_from_input


parser = ArgumentParser()
parser.add_argument(
    "data",
    type=open,
)
parser.add_argument(
    "-m", "--multi",
    action="store_true"
)

if __name__ == "__main__":
    args = parser.parse_args()
    directions, map = get_directions_and_map_from_input(args.data)
    if args.multi:
        print(map.get_multi_step_count("A", "Z", directions))
    else:
        print(map.get_step_count("AAA", "ZZZ", directions))
