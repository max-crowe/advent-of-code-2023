from io import TextIOBase

from .graph import Graph, Node


def is_multiple_weight(x: int, y: int, grid: list[list[str]]) -> bool:
    return all(row[x] == "." for row in grid) or all(item == "." for item in grid[y])


def get_graph_from_input_data(input_data: TextIOBase, weight_coefficient: int = 2) -> Graph:
    grid = [list(line.strip()) for line in input_data]
    width = len(grid[0])
    height = len(grid)
    graph = Graph()
    nodes = [[Node(x_index, y_index) for x_index in range(width)] for y_index in range(height)]
    for y_index in range(height):
        for x_index in range(width):
            node = nodes[y_index][x_index]
            graph.nodes.add(node)
            if grid[y_index][x_index] == "#":
                graph.target_nodes.append(node)
            weight = weight_coefficient if is_multiple_weight(x_index, y_index, grid) else 1
            for offset in (1, -1):
                x_offset = x_index + offset
                y_offset = y_index + offset
                if 0 <= x_offset < width:
                    nodes[y_index][x_offset].connect_to(node, weight)
                if 0 <= y_offset < height:
                    nodes[y_offset][x_index].connect_to(node, weight)
    return graph
