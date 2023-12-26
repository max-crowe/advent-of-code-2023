#!/usr/bin/env python

import sys
from argparse import ArgumentParser
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from day17.parser import get_graph_from_input_data


parser = ArgumentParser()
parser.add_argument(
    "data",
    type=open,
)

if __name__ == "__main__":
    args = parser.parse_args()
    graph = get_graph_from_input_data(args.data)
    print(graph.get_shortest_path(graph[0, 0], graph[graph.width - 1, graph.height - 1]))
