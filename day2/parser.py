import re
from collections.abc import Generator
from io import TextIOBase

from .game import COLORS, Game, CubeSet


class InvalidDataError(ValueError):
    pass


def get_games_from_input(input_data: TextIOBase) -> Generator[Game]:
    for line in input_data:
        match = re.search(r"^Game (\d+):", line)
        if not match:
            raise InvalidDataError
        game_id = int(match.group(1))
        rounds: list[CubeSet] = []
        all_round_data = line[line.index(":") + 1:].strip()
        for round_data in all_round_data.split(";"):
            round = CubeSet()
            for color in COLORS:
                match = re.search(r"(\d+) {}".format(color), round_data)
                if match:
                    setattr(round, color, int(match.group(1)))
            if round.red or round.blue or round.green:
                rounds.append(round)
        yield Game(id=game_id, rounds=rounds)
