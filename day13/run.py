#!/usr/bin/env python

import sys
from argparse import ArgumentParser
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from day13.parser import iter_maps_from_input
from day13.maps import Orientation


parser = ArgumentParser()
parser.add_argument(
    "data",
    type=open,
)
parser.add_argument(
    "-d", "--difference-count",
    type=int,
    default=0,
)

if __name__ == "__main__":
    args = parser.parse_args()
    result = 0
    for map in iter_maps_from_input(args.data):
        orientation, index = map.find_axis_of_reflection(args.difference_count)
        if orientation is Orientation.VERTICAL:
            result += 100 * (index + 1)
        else:
            result += index + 1
    print(result)
