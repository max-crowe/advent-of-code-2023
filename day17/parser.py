from io import TextIOBase

from .graph import Direction, Graph, Node


def get_graph_from_input_data(input_data: TextIOBase) -> Graph:
    return Graph(
        [
            [Node(col_index, row_index, int(char)) for col_index, char in enumerate(line.strip())]
            for row_index, line in enumerate(input_data)
        ]
    )
