from dataclasses import dataclass, field
from enum import StrEnum


class NodeType(StrEnum):
    EDGE = "#"
    UNKNOWN = "."
    INTERIOR = "I"


class Direction(StrEnum):
    NORTH = "U"
    EAST = "R"
    SOUTH = "D"
    WEST = "L"


@dataclass
class Node:
    x: int
    y: int
    type: NodeType = NodeType.UNKNOWN
    linked_nodes: dict[Direction, "Node"] = field(default_factory=dict)

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __repr__(self) -> str:
        return f"Node({self.x}, {self.y}, {self.type})"

    def link_to(self, other: "Node", direction: Direction):
        self.linked_nodes[direction] = other


class Graph:
    def __init__(self, edge_nodes: list[Node]):
        edge_node_index, width, height = self.get_compensated_index_and_dimensions(edge_nodes)
        self.nodes: list[list[Node]] = []
        for row_index in range(height):
            row: list[Node] = []
            self.nodes.append(row)
            for col_index in range(width):
                try:
                    row.append(edge_node_index[col_index, row_index])
                except KeyError:
                    row.append(Node(col_index, row_index))
        for row_index in range(height):
            for col_index in range(width):
                if col_index > 0 and Direction.WEST not in self[col_index, row_index].linked_nodes:
                    self[col_index, row_index].linked_nodes[Direction.WEST] = self[col_index - 1, row_index]
                if col_index < width - 1 and Direction.EAST not in self[col_index, row_index].linked_nodes:
                    self[col_index, row_index].linked_nodes[Direction.EAST] = self[col_index + 1, row_index]
                if row_index > 0 and Direction.NORTH not in self[col_index, row_index].linked_nodes:
                    self[col_index, row_index].linked_nodes[Direction.NORTH] = self[col_index, row_index - 1]
                if row_index < height - 1 and Direction.SOUTH not in self[col_index, row_index].linked_nodes:
                    self[col_index, row_index].linked_nodes[Direction.SOUTH] = self[col_index, row_index + 1]
        self.edge_nodes = set(edge_node_index.values())

    def __str__(self) -> str:
        return "\n".join(
            "".join([node.type for node in row]) for row in self.nodes
        )

    def __getitem__(self, coords: tuple[int, int]) -> Node:
        return self.nodes[coords[1]][coords[0]]

    @staticmethod
    def get_compensated_index_and_dimensions(edge_nodes: list[Node]) -> tuple[dict[tuple[int, int], Node], int, int]:
        min_col: int | None = None
        max_col: int | None = None
        min_row: int | None = None
        max_row: int | None = None
        index: dict[tuple[int, int], Node] = {}
        for node in edge_nodes:
            if min_col is None or node.x < min_col:
                min_col = node.x
            if max_col is None or node.x > max_col:
                max_col = node.x
            if min_row is None or node.y < min_row:
                min_row = node.y
            if max_row is None or node.y > max_row:
                max_row = node.y
        col_offset = 0 if min_col >= 0 else min_col * -1
        row_offset = 0 if min_row >= 0 else min_row * -1
        for node in edge_nodes:
            node.x += col_offset
            node.y += row_offset
            index[node.x, node.y] = node
        return index, (max_col - min_col) + 1, (max_row - min_row) + 1

    def fill_contiguous_section(self, start_node: Node, section: set[Node]):
        unexpanded_nodes: set[Node] = {start_node}
        while unexpanded_nodes:
            node = unexpanded_nodes.pop()
            section.add(node)
            unexpanded_nodes |= set(
                filter(
                    lambda node: node not in section and node not in self.edge_nodes,
                    node.linked_nodes.values()
                )
            )

    def get_interior_nodes(self) -> set[Node]:
        interior_nodes: set[Node] = set()
        found_entry = False
        for row in self.nodes:
            for node in row:
                if (
                    node in self.edge_nodes
                    and (node.x == 0 or self[node.x - 1, node.y] not in self.edge_nodes)
                    and self[node.x + 1, node.y] not in self.edge_nodes
                ):
                    found_entry = True
                    self.fill_contiguous_section(self[node.x + 1, node.y], interior_nodes)
                    break
            if found_entry:
                break
        return interior_nodes

    def mark_interior_nodes(self):
        for node in self.get_interior_nodes():
            node.type = NodeType.INTERIOR

    def get_area(self) -> int:
        return len(self.get_interior_nodes()) + len(self.edge_nodes)

    @property
    def width(self) -> int:
        return len(self.nodes[0])

    @property
    def height(self) -> int:
        return len(self.nodes)
