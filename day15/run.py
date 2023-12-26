#!/usr/bin/env python

import sys
from argparse import ArgumentParser
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from day15.hashing import get_hash
from day15.orchestration import BoxOrchestrator
from day15.parser import get_values_from_input_data


parser = ArgumentParser()
parser.add_argument(
    "data",
    type=open,
)
parser.add_argument(
    "-m", "--mode",
    choices=["hash-sum", "focusing-power"]
)

if __name__ == "__main__":
    args = parser.parse_args()
    steps = get_values_from_input_data(args.data)
    if args.mode == "hash-sum":
        print(sum(get_hash(value) for value in steps))
    else:
        orchestrator = BoxOrchestrator()
        for step in steps:
            orchestrator.handle_step(step)
        print(orchestrator.get_focal_power())
