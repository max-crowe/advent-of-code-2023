from io import TextIOBase

from .mapping import RangeSet, RangeSetOrchestrator


def get_seeds_and_orchestrator_from_input(input_data: TextIOBase) -> tuple[list[int], RangeSetOrchestrator]:
    seeds: list[int] = []
    orchestrator = RangeSetOrchestrator()
    current_set: RangeSet | None = None
    for line in input_data:
        line = line.strip()
        if line.startswith("seeds:"):
            seeds.extend([int(seed_value) for seed_value in line[7:].split(" ")])
        elif line.endswith("map:"):
            map_description, _, _ = line.partition(" ")
            source, _, destination = map_description.partition("-to-")
            current_set = RangeSet(source, destination)
            orchestrator.add_range_set(current_set)
        elif line:
            assert current_set is not None
            values = [int(value) for value in line.split(" ")]
            assert len(values) == 3
            current_set.add_range(*tuple(values))
    return seeds, orchestrator


def get_seed_ranges_and_orchestrator_from_input(input_data: TextIOBase) -> tuple[list[range], RangeSetOrchestrator]:
    range_values, orchestrator = get_seeds_and_orchestrator_from_input(input_data)
    ranges = [
        range(range_values[value_idx], range_values[value_idx] + range_values[value_idx + 1])
        for value_idx in range(0, len(range_values), 2)
    ]
    return ranges, orchestrator
