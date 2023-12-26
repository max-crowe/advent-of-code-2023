import operator
from dataclasses import dataclass
from enum import Enum, StrEnum, auto
from itertools import chain


class Direction(Enum):
    NORTH = auto()
    WEST = auto()
    SOUTH = auto()
    EAST = auto()


class ObstacleType(StrEnum):
    MOBILE = "O"
    IMMOBILE = "#"


@dataclass
class Map:
    data: list[list[ObstacleType | None]]

    def __str__(self):
        return "\n".join("".join("." if obj is None else str(obj) for obj in row) for row in self.data)

    def __getitem__(self, coords: tuple[int, int]) -> ObstacleType | None:
        return self.data[coords[1]][coords[0]]

    def __setitem__(self, coords: tuple[int, int], item: ObstacleType):
        if self[coords] is not None:
            raise ValueError(f"Item already exists at position {coords}")
        self.data[coords[1]][coords[0]] = item

    def __delitem__(self, coords: tuple[int, int]):
        self.data[coords[1]][coords[0]] = None

    def get_current_hash(self) -> int:
        return hash(tuple(chain.from_iterable(self.data)))

    def shift_obstacles(self, direction: Direction = Direction.NORTH):
        match direction:
            case Direction.NORTH | Direction.SOUTH:
                for col_index in range(self.width):
                    if direction is Direction.NORTH:
                        last_unobstructed_position = 0
                        range_ = range(self.height)
                        step_offset = 1
                        comp_fn = operator.gt
                    else:
                        last_unobstructed_position = self.height - 1
                        range_ = range(self.height - 1, -1, -1)
                        step_offset = -1
                        comp_fn = operator.lt
                    for row_index in range_:
                        if self[col_index, row_index] is not None:
                            if self[col_index, row_index] is ObstacleType.IMMOBILE:
                                last_unobstructed_position = row_index + step_offset
                            else:
                                if comp_fn(row_index, last_unobstructed_position):
                                    self[col_index, last_unobstructed_position] = ObstacleType.MOBILE
                                    del self[col_index, row_index]
                                last_unobstructed_position += step_offset
            case _:
                for row_index in range(self.height):
                    if direction is Direction.WEST:
                        last_unobstructed_position = 0
                        range_ = range(self.width)
                        step_offset = 1
                        comp_fn = operator.gt
                    else:
                        last_unobstructed_position = self.width - 1
                        range_ = range(self.width - 1, -1, -1)
                        step_offset = -1
                        comp_fn = operator.lt
                    for col_index in range_:
                        if self[col_index, row_index] is not None:
                            if self[col_index, row_index] is ObstacleType.IMMOBILE:
                                last_unobstructed_position = col_index + step_offset
                            else:
                                if comp_fn(col_index, last_unobstructed_position):
                                    self[last_unobstructed_position, row_index] = ObstacleType.MOBILE
                                    del self[col_index, row_index]
                                last_unobstructed_position += step_offset

    def run_cycle(self):
        for direction in Direction:
            self.shift_obstacles(direction)

    def run_cycles(self, cycle_count: int):
        patterns: dict[int, int] = {}
        for i in range(1, cycle_count + 1):
            self.run_cycle()
            current_hash = self.get_current_hash()
            if current_hash not in patterns:
                patterns[current_hash] = i
            elif (cycle_count - patterns[current_hash]) % (i - patterns[current_hash]) == 0:
                break

    def get_total_load(self) -> int:
        load = 0
        for row_index in range(self.height):
            load += len(
                [item for item in self.data[row_index] if item is ObstacleType.MOBILE]
            ) * (self.height - row_index)
        return load

    @property
    def width(self) -> int:
        return len(self.data[0])

    @property
    def height(self) -> int:
        return len(self.data)
