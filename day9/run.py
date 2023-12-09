#!/usr/bin/env python

import sys
from argparse import ArgumentParser
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from day9.parser import iter_sequences_from_input
from day9.predictor import extrapolate


parser = ArgumentParser()
parser.add_argument(
    "data",
    type=open,
)
parser.add_argument(
    "--left",
    action="store_true"
)

if __name__ == "__main__":
    args = parser.parse_args()
    print(sum(extrapolate(seq, args.left) for seq in iter_sequences_from_input(args.data)))
