#!/usr/bin/env python

import sys
from argparse import ArgumentParser
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from day11.graph import Node
from day11.parser import get_graph_from_input_data


parser = ArgumentParser()
parser.add_argument(
    "data",
    type=open,
)
parser.add_argument(
    "-w", "--weight",
    type=int,
    default=2,
)

if __name__ == "__main__":
    args = parser.parse_args()
    graph = get_graph_from_input_data(args.data, args.weight)
    print(graph.get_sum_of_distances_between_all_targets())

