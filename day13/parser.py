from collections.abc import Generator
from io import TextIOBase

from .maps import Map, TerrainType


def iter_maps_from_input(input_data: TextIOBase) -> Generator[Map]:
    current_map: list[list[TerrainType]] = []
    for line in input_data:
        line = line.strip()
        if line:
            current_map.append([TerrainType(c) for c in line])
        else:
            yield Map(current_map)
            current_map = []
    yield Map(current_map)
