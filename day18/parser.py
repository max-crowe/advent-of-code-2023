import re
from io import TextIOBase

from .graph import Direction, Graph, Node, NodeType


def parse_hex_param(hex_param) -> tuple[int, Direction]:
    direction: Direction
    match hex_param[-1]:
        case "0":
            direction = Direction.EAST
        case "1":
            direction = Direction.SOUTH
        case "2":
            direction = Direction.WEST
        case "3":
            direction = Direction.NORTH
        case _:
            raise ValueError(f"Unexpected value {hex_param[-1]}")
    return int(hex_param[:5], base=16), direction


def get_graph_from_input_data(input_data: TextIOBase, use_hex_param: bool = False) -> Graph:
    x = 0
    y = 0
    current_node = Node(x, y, type=NodeType.EDGE)
    edge_nodes: dict[tuple[int, int], Node] = {(x, y): current_node}
    for line in input_data:
        match = re.match(r"^([RDLU]) (\d+) \(#([a-f0-9]{6})\)", line)
        assert match is not None
        if use_hex_param:
            step_count, direction = parse_hex_param(match.group(3))
        else:
            direction = Direction(match.group(1))
            step_count = int(match.group(2))
        for _ in range(step_count):
            match direction:
                case Direction.NORTH:
                    y -= 1
                case Direction.SOUTH:
                    y += 1
                case Direction.EAST:
                    x += 1
                case _:
                    x -= 1
            next_node = edge_nodes.get((x, y), Node(x, y, type=NodeType.EDGE))
            current_node.link_to(next_node, direction)
            edge_nodes[x, y] = next_node
            current_node = next_node
    return Graph(list(edge_nodes.values()))
