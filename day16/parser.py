from io import TextIOBase

from .graph import Graph, Node, NodeType


def get_graph_from_input_data(input_data: TextIOBase) -> Graph:
    nodes: list[list[Node]] = []
    for row_index, line in enumerate(input_data):
        node_row: list[Node] = []
        nodes.append(node_row)
        for col_index, char in enumerate(line.strip()):
            node_type: NodeType
            match char:
                case "-" | "|":
                    node_type = NodeType.SPLITTER
                case "/" | "\\":
                    node_type = NodeType.MIRROR
                case _:
                    node_type = NodeType.EMPTY
            node_row.append(Node(col_index, row_index, node_type, char))
    graph = Graph(nodes)
    graph.link_nodes()
    return graph
