from io import TextIOBase

from .graph import Direction, Graph, Node


def get_graph_from_input_data(input_data: TextIOBase) -> Graph:
    start_pos: tuple[int, int] | None = None
    nodes: list[list[Node | None]] = []
    for y_pos, line in enumerate(input_data):
        node_row: list[Node | None] = []
        for x_pos, char in enumerate(line.strip()):
            match char:
                case ".":
                    node_row.append(None)
                case "|":
                    node_row.append(Node(x_pos, y_pos, (Direction.NORTH, Direction.SOUTH)))
                case "-":
                    node_row.append(Node(x_pos, y_pos, (Direction.EAST, Direction.WEST)))
                case "L":
                    node_row.append(Node(x_pos, y_pos, (Direction.NORTH, Direction.EAST)))
                case "J":
                    node_row.append(Node(x_pos, y_pos, (Direction.NORTH, Direction.WEST)))
                case "7":
                    node_row.append(Node(x_pos, y_pos, (Direction.SOUTH, Direction.WEST)))
                case "F":
                    node_row.append(Node(x_pos, y_pos, (Direction.SOUTH, Direction.EAST)))
                case "S":
                    assert start_pos is None
                    start_pos = (x_pos, y_pos)
                    node_row.append(None)
                case _:
                    raise ValueError(f"Unexpected symbol: {char}")
        nodes.append(node_row)
    return Graph(nodes, start_pos)
