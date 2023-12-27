#!/usr/bin/env python

import sys
from argparse import ArgumentParser
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from day19.parser import get_orchestrator_and_part_list_from_input_data
from day19.workflow import Result


parser = ArgumentParser()
parser.add_argument(
    "data",
    type=open,
)

if __name__ == "__main__":
    args = parser.parse_args()
    orchestrator, parts = get_orchestrator_and_part_list_from_input_data(args.data)
    print(sum(int(part) for part in parts if orchestrator.entry_workflow(part) is Result.ACCEPTED))
