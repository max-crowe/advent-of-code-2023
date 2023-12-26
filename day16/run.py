#!/usr/bin/env python

import sys
from argparse import ArgumentParser
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from day16.graph import Direction
from day16.parser import get_graph_from_input_data


parser = ArgumentParser()
parser.add_argument(
    "data",
    type=open,
)
parser.add_argument(
    "-l", "--longest",
    action="store_true"
)

if __name__ == "__main__":
    args = parser.parse_args()
    graph = get_graph_from_input_data(args.data)
    if args.longest:
        path = graph.find_longest_traversal_path()
    else:
        path = graph.traverse((0, 0), Direction.EAST)
    print(len(path))
