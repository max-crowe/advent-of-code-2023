from enum import StrEnum
from functools import reduce
from itertools import cycle

ITER_LIMIT = 1000000000


class Directions(StrEnum):
    LEFT = "L"
    RIGHT = "R"


class Map:
    def __init__(self):
        self.nodes: dict[str, tuple[str, str]] = {}

    def add_node(self, key: str, options: tuple[str, str]):
        self.nodes[key] = options

    def get_next_key(self, key: str, direction: Directions) -> str:
        return self.nodes[key][0 if direction is Directions.LEFT else 1]

    def get_step_count(self, start: str, end: str, directions: str) -> int:
        step_count = 0
        directions_iter = cycle(directions)
        current_key = start
        while current_key != end:
            direction = next(directions_iter)
            step_count += 1
            if step_count == ITER_LIMIT:
                raise RuntimeError("Iterations reached limit")
            current_key = self.get_next_key(current_key, Directions(direction))
        return step_count

    def get_multi_step_count(self, start_suffix: str, end_suffix: str, directions: str) -> int:
        start_keys = [key for key in self.nodes if key.endswith(start_suffix)]
        cycle_lengths: list[int] = []
        for start_key in start_keys:
            step_count = 0
            directions_iter = cycle(directions)
            current_key = start_key
            while True:
                if current_key.endswith(end_suffix):
                    cycle_lengths.append(step_count)
                    break
                direction = next(directions_iter)
                step_count += 1
                if step_count == ITER_LIMIT:
                    raise RuntimeError("Iterations reached limit")
                current_key = self.get_next_key(current_key, Directions(direction))
        lcm = get_lcm(cycle_lengths[0], cycle_lengths[1])
        for i in range(2, len(cycle_lengths)):
            lcm = get_lcm(lcm, cycle_lengths[i])
        return lcm


def get_gcd(a: int, b: int) -> int:
    if a == 0:
        return b
    return get_gcd(b % a, a)


def get_lcm(a: int, b: int) -> int:
    lcm = a * b / get_gcd(a, b)
    assert lcm % 1 == 0
    return int(lcm)
