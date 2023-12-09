import re
from io import TextIOBase

from .map import Map

NODE_PATTERN = re.compile(r"^([A-Z0-9]+) = \(([A-Z0-9]+), ([A-Z0-9]+)\)$")


def get_directions_and_map_from_input(input_data: TextIOBase) -> tuple[str, Map]:
    directions = ""
    map = Map()
    for line in input_data:
        line = line.strip()
        if match := NODE_PATTERN.match(line):
            map.add_node(match.group(1), (match.group(2), match.group(3)))
        elif line:
            directions = line
    assert len(directions) > 0
    return directions, map
