from collections.abc import Generator
from dataclasses import dataclass
from enum import Enum, auto
from functools import cached_property


class DataType(Enum):
    NUMBER = auto()
    SYMBOL = auto()


@dataclass
class Element:
    start: int
    value: str

    @cached_property
    def data_type(self) -> DataType:
        return DataType.NUMBER if all(char.isdigit() for char in self.value) else DataType.SYMBOL

    @cached_property
    def range(self) -> range:
        return range(self.start, self.start + len(self.value))

    @cached_property
    def is_gear(self) -> bool:
        return self.value == "*"


@dataclass
class Line:
    elements: list[Element]

    def __len__(self) -> int:
        if self.elements:
            return self.elements[-1].start + len(self.elements[-1].value)
        return 0

    def get_elements_in_range(self, check_range: range) -> list[Element]:
        elements: list[Element] = []
        for element in self.elements:
            if element.start > check_range.stop:
                break
            if (
                element.start <= check_range.start < element.range.stop
            ) or (
                check_range.start <= element.start < check_range.stop
            ):
                elements.append(element)
        return elements

    def get_data_types_in_range(self, check_range: range) -> set[DataType]:
        return set(element.data_type for element in self.get_elements_in_range(check_range))


@dataclass
class Schematic:
    lines: list[Line]

    def get_part_numbers(self) -> Generator[int]:
        for line_number, line in enumerate(self.lines):
            for element in line.elements:
                if element.data_type is DataType.NUMBER:
                    is_part_number = False
                    adjacency_range = range(element.start - 1 if element.start else 0, element.range.stop + 1)
                    if line_number > 0:
                        is_part_number = DataType.SYMBOL in self.lines[line_number - 1].get_data_types_in_range(
                            adjacency_range
                        )
                    if not is_part_number and line_number < len(self.lines) - 1:
                        is_part_number = DataType.SYMBOL in self.lines[line_number + 1].get_data_types_in_range(
                            adjacency_range
                        )
                    if not is_part_number and element.start > 0:
                        is_part_number = DataType.SYMBOL in line.get_data_types_in_range(
                            range(element.start - 1, element.start)
                        )
                    if not is_part_number:
                        is_part_number = DataType.SYMBOL in line.get_data_types_in_range(
                            range(element.range.stop, element.range.stop + 1)
                        )
                    if is_part_number:
                        yield int(element.value)

    def get_gear_ratios(self) -> Generator[int]:
        for line_number, line in enumerate(self.lines):
            for element in line.elements:
                if element.is_gear:
                    adjacent_numbers: list[int] = []
                    adjacency_range = range(element.start - 1 if element.start else 0, element.range.stop + 1)
                    if line_number > 0:
                        adjacent_numbers.extend(
                            [
                                int(element.value)
                                for element in self.lines[line_number - 1].get_elements_in_range(adjacency_range)
                                if element.data_type is DataType.NUMBER
                            ]
                        )
                    if line_number < len(self.lines) - 1:
                        adjacent_numbers.extend(
                            [
                                int(element.value)
                                for element in self.lines[line_number + 1].get_elements_in_range(adjacency_range)
                                if element.data_type is DataType.NUMBER
                            ]
                        )
                    if element.start > 0:
                        adjacent_numbers.extend(
                            [
                                int(element.value)
                                for element in line.get_elements_in_range(range(element.start - 1, element.start))
                                if element.data_type is DataType.NUMBER
                            ]
                        )
                    adjacent_numbers.extend(
                        [
                            int(element.value)
                            for element in line.get_elements_in_range(range(element.range.stop, element.range.stop + 1))
                            if element.data_type is DataType.NUMBER
                        ]
                    )
                    if len(adjacent_numbers) == 2:
                        yield adjacent_numbers[0] * adjacent_numbers[1]
