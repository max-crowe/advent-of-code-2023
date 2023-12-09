from dataclasses import dataclass, fields


@dataclass
class CubeSet:
    red: int = 0
    green: int = 0
    blue: int = 0


@dataclass
class Game:
    id: int
    rounds: list[CubeSet]

    def get_minimum_viable_set(self) -> CubeSet:
        minimum_viable_set = CubeSet()
        for round in self.rounds:
            minimum_viable_set.red = max(minimum_viable_set.red, round.red)
            minimum_viable_set.green = max(minimum_viable_set.green, round.green)
            minimum_viable_set.blue = max(minimum_viable_set.blue, round.blue)
        return minimum_viable_set


COLORS = [field.name for field in fields(CubeSet)]
