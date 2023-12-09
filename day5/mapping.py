from collections.abc import Generator
from functools import cached_property


def find_range_index(key: int, range_container: list[range]) -> int:
    for idx, range_obj in enumerate(range_container):
        if range_obj.start <= key < range_obj.stop:
            return idx
    raise ValueError


def get_intersections(source: list[range], target: list[range]) -> list[range]:
    intersections: list[range] = []
    target = sorted(target, key=lambda range_obj: range_obj.start)
    for range_obj in source:
        for candidate in target:
            if candidate.start >= range_obj.stop:
                break
            if candidate.start <= range_obj.start < candidate.stop:
                intersections.append(
                    range(range_obj.start, min(range_obj.stop, candidate.stop))
                )
            elif range_obj.start <= candidate.start < range_obj.stop:
                intersections.append(
                    range(candidate.start, min(range_obj.stop, candidate.stop))
                )
    return intersections



class RangeSet:
    def __init__(self, source_category: str, destination_category: str):
        self.source_category = source_category
        self.destination_category = destination_category
        self.source_ranges: list[range] = []
        self.destination_ranges: list[range] = []

    def get_mapped_value(self, key: int, reverse: bool = False) -> int:
        if reverse:
            range_container, other_range_container = self.destination_ranges, self.source_ranges
        else:
            range_container, other_range_container = self.source_ranges, self.destination_ranges
        try:
            range_index = find_range_index(key, range_container)
        except ValueError:
            return key
        offset = key - range_container[range_index].start
        return other_range_container[range_index].start + offset

    def find_source_range_index(self, key: int) -> int:
        try:
            return find_range_index(key, self.source_ranges)
        except ValueError:
            raise ValueError(f"No suitable {self.source_category} range found for key {key}")

    def find_destination_range_index(self, key: int) -> int:
        try:
            return find_range_index(key, self.destination_ranges)
        except ValueError:
            raise ValueError(f"No suitable {self.destination_category} range found for key {key}")

    def add_range(self, destination_start: int, source_start: int, length: int):
        self.source_ranges.append(range(source_start, source_start + length))
        self.destination_ranges.append(range(destination_start, destination_start + length))

    @cached_property
    def sorted_destination_range_indices(self) -> list[int]:
        destination_ranges = list(enumerate(self.destination_ranges))
        destination_ranges.sort(key=lambda pair: pair[1].start)
        return [pair[0] for pair in destination_ranges]


class RangeSetOrchestrator:
    def __init__(self):
        self.lookup_table: dict[str, RangeSet] = {}
        self.lookup_table_by_destination: dict[str, RangeSet] = {}

    def add_range_set(self, range_set: RangeSet):
        self.lookup_table[range_set.source_category] = range_set
        self.lookup_table_by_destination[range_set.destination_category] = range_set

    def get_mapped_value(self, key: int, source_category: str) -> int:
        range_set: RangeSet
        while source_category in self.lookup_table:
            range_set = self.lookup_table[source_category]
            key = range_set.get_mapped_value(key)
            source_category = range_set.destination_category
        return key

    def get_reverse_mapped_value(self, key: int, destination_category: str) -> int:
        range_set: RangeSet
        while destination_category in self.lookup_table_by_destination:
            range_set = self.lookup_table_by_destination[destination_category]
            key = range_set.get_mapped_value(key, reverse=True)
            destination_category = range_set.source_category
        return key
