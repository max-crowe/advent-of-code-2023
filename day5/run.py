#!/usr/bin/env python

import sys
from argparse import ArgumentParser
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from day5.mapping import find_range_index
from day5.parser import get_seeds_and_orchestrator_from_input, get_seed_ranges_and_orchestrator_from_input


parser = ArgumentParser()
parser.add_argument(
    "data",
    type=open,
)
parser.add_argument(
    "--seeds-as-ranges",
    action="store_true"
)

if __name__ == "__main__":
    args = parser.parse_args()
    if args.seeds_as_ranges:
        seed_ranges, orchestrator = get_seed_ranges_and_orchestrator_from_input(args.data)
        limit = orchestrator.lookup_table_by_destination["location"].destination_ranges[
            orchestrator.lookup_table_by_destination["location"].sorted_destination_range_indices[-1]
        ].stop
        for location_id in range(0, limit):
            seed_value = orchestrator.get_reverse_mapped_value(location_id, "location")
            try:
                find_range_index(seed_value, seed_ranges)
            except ValueError:
                pass
            else:
                print(location_id)
                break
    else:
        seeds, orchestrator = get_seeds_and_orchestrator_from_input(args.data)
        print(min(
            [orchestrator.get_mapped_value(seed, "seed") for seed in seeds]
        ))
