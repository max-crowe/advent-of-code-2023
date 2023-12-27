#!/usr/bin/env python

import sys
from argparse import ArgumentParser
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from day18.parser import get_graph_from_input_data


parser = ArgumentParser()
parser.add_argument(
    "data",
    type=open,
)
parser.add_argument(
    "-d", "--debug",
    action="store_true"
)

if __name__ == "__main__":
    args = parser.parse_args()
    graph = get_graph_from_input_data(args.data)
    if args.debug:
        graph.mark_interior_nodes()
        print(graph)
    else:
        print(graph.get_area())
