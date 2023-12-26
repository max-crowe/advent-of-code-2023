from io import TextIOBase

from .maps import Map, ObstacleType


def get_map_from_input_data(input_data: TextIOBase) -> Map:
    return Map([[None if c == "." else ObstacleType(c) for c in line.strip()] for line in input_data])
