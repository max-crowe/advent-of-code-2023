from dataclasses import dataclass
from enum import StrEnum


class Condition(StrEnum):
    OPERATIONAL = "."
    BROKEN = "#"
    UNKNOWN = "?"


@dataclass
class Group:
    condition: Condition
    size: int


@dataclass
class Record:
    conditions: list[Condition]

    def consume_contiguous_group(self, from_index: int, target_size: int) -> list[Condition] | None:
        group: list[Condition] = []
        condition: Condition = Condition.UNKNOWN
        for current_index in range(from_index, len(self.conditions) - from_index):
            if condition is condition.UNKNOWN:
                condition = self.conditions[current_index]
            if self.conditions[current_index] is not condition:
                if condition is not Condition.UNKNOWN:
                    return group if condition is Condition.OPERATIONAL or len(group) >= target_size else None
            group.append(self.conditions[current_index])
            if condition is Condition.OPERATIONAL or len(group) == target_size:
                return group

    def find_viable_arrangements(self, sizes: list[int], from_index: int = 0) -> list[Condition] | None:
        current_offset: int = 0
        size_under_test = sizes.pop(0)
        current_group: list[Condition] = []
