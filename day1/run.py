#!/usr/bin/env python
import sys
from argparse import ArgumentParser
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from day1.handler import handle, handle_with_replacement

parser = ArgumentParser()
parser.add_argument(
    "data",
    type=open,
)
parser.add_argument(
    "-r", "--replace",
    action="store_true",
)


if __name__ == "__main__":
    args = parser.parse_args()
    result = 0
    for line in args.data:
        if args.replace:
            result += handle_with_replacement(line)
        else:
            result += handle(line)
    print(result)
