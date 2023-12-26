from dataclasses import dataclass
from enum import Enum, StrEnum, auto
from math import floor


class Orientation(Enum):
    HORIZONTAL = auto()
    VERTICAL = auto()


class TerrainType(StrEnum):
    ASH = "."
    ROCK = "#"


@dataclass
class Map:
    data: list[list[TerrainType]]

    def __getitem__(self, coords: tuple[int, int]) -> TerrainType:
        return self.data[coords[1]][coords[0]]

    def offset_in_bounds(self, index: int, offset: int, orientation: Orientation) -> bool:
        return index + offset < (
            self.height if orientation is Orientation.VERTICAL else self.width
        ) and index - (offset - 1) >= 0

    def is_reflection(self, index: int, orientation: Orientation, difference_count: int = 0) -> bool:
        offset = 1
        accumulated_differences = 0
        while self.offset_in_bounds(index, offset, orientation):
            if orientation is Orientation.VERTICAL:
                row = self.data[index - (offset - 1)]
                comp_row = self.data[index + offset]
                accumulated_differences += len(
                    [row[i] for i in range(self.width) if row[i] is not comp_row[i]]
                )
            else:
                column = [self[index - (offset - 1), y] for y in range(self.height)]
                comp_column = [self[index + offset, y] for y in range(self.height)]
                accumulated_differences += len(
                    [column[i] for i in range(self.height) if column[i] is not comp_column[i]]
                )
            if accumulated_differences > difference_count:
                break
            offset += 1
        return accumulated_differences == difference_count

    def find_axis_of_reflection(self, difference_count: int = 0) -> tuple[Orientation, int]:
        start_row = floor(self.height / 2)
        for row in range(start_row, self.height - 1):
            if self.is_reflection(row, Orientation.VERTICAL, difference_count):
                return Orientation.VERTICAL, row
        for row in range(start_row - 1, -1, -1):
            if self.is_reflection(row, Orientation.VERTICAL, difference_count):
                return Orientation.VERTICAL, row
        start_column = floor(self.width / 2)
        for column in range(start_column, self.width - 1):
            if self.is_reflection(column, Orientation.HORIZONTAL, difference_count):
                return Orientation.HORIZONTAL, column
        for column in range(start_column - 1, -1, -1):
            if self.is_reflection(column, Orientation.HORIZONTAL, difference_count):
                return Orientation.HORIZONTAL, column
        raise ValueError("No axis of reflection found")

    @property
    def width(self) -> int:
        return len(self.data[0])

    @property
    def height(self) -> int:
        return len(self.data)
