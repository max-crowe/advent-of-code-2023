#!/usr/bin/env python
import sys
from argparse import ArgumentParser
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from day3.parser import get_schematic_from_input

parser = ArgumentParser()
parser.add_argument(
    "data",
    type=open,
)
parser.add_argument(
    "-m", "--mode",
    choices=["part-numbers", "gear-ratios"]
)

if __name__ == "__main__":
    args = parser.parse_args()
    schematic = get_schematic_from_input(args.data)
    if args.mode == "part-numbers":
        print(sum(schematic.get_part_numbers()))
    else:
        print(sum(schematic.get_gear_ratios()))
