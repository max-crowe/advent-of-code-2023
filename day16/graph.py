from dataclasses import dataclass, field
from enum import Enum, auto


class Direction(Enum):
    NORTH = auto()
    WEST = auto()
    SOUTH = auto()
    EAST = auto()


class NodeType(Enum):
    EMPTY = auto()
    MIRROR = auto()
    SPLITTER = auto()


@dataclass(frozen=True)
class Node:
    x: int
    y: int
    type: NodeType
    symbol: str
    linked_nodes: dict[Direction, "Node | None"] = field(default_factory=dict)

    def __repr__(self) -> str:
        return f"Node({self.x}, {self.y}, {self.type}, {self.symbol})"

    def __hash__(self):
        return hash((self.x, self.y))

    def get_linked_nodes(self, direction: Direction) -> list[tuple["Node", Direction]]:
        linked_nodes: list[tuple["Node", Direction]] = []
        if self.type is NodeType.MIRROR:
            next_direction: Direction
            match self.symbol:
                case "\\":
                    match direction:
                        case Direction.NORTH:
                            next_direction = Direction.WEST
                        case Direction.WEST:
                            next_direction = Direction.NORTH
                        case Direction.SOUTH:
                            next_direction = Direction.EAST
                        case Direction.EAST:
                            next_direction = Direction.SOUTH
                case "/":
                    match direction:
                        case Direction.NORTH:
                            next_direction = Direction.EAST
                        case Direction.WEST:
                            next_direction = Direction.SOUTH
                        case Direction.SOUTH:
                            next_direction = Direction.WEST
                        case Direction.EAST:
                            next_direction = Direction.NORTH
            if self.linked_nodes[next_direction] is not None:
                linked_nodes.append((self.linked_nodes[next_direction], next_direction))
            return linked_nodes
        elif self.type is NodeType.SPLITTER:
            split_directions: list[Direction] = []
            match self.symbol:
                case "|":
                    if direction is Direction.EAST or direction is Direction.WEST:
                        split_directions.extend([Direction.NORTH, Direction.SOUTH])
                case "-":
                    if direction is Direction.NORTH or direction is Direction.SOUTH:
                        split_directions.extend([Direction.EAST, Direction.WEST])
            if split_directions:
                for next_direction in split_directions:
                    if self.linked_nodes[next_direction] is not None:
                        linked_nodes.append(
                            (self.linked_nodes[next_direction], next_direction)
                        )
                return linked_nodes
        if self.linked_nodes[direction] is not None:
            linked_nodes.append((self.linked_nodes[direction], direction))
        return linked_nodes

@dataclass
class Graph:
    nodes: list[list[Node]]

    def __getitem__(self, coords: tuple[int, int]) -> Node:
        return self.nodes[coords[1]][coords[0]]

    def link_nodes(self):
        for row_index in range(self.height):
            for col_index in range(self.width):
                node = self[col_index, row_index]
                if node.symbol != "-":
                    node.linked_nodes[Direction.NORTH] = (
                        None if row_index == 0 else self[col_index, row_index - 1]
                    )
                    node.linked_nodes[Direction.SOUTH] = (
                        None if row_index == self.height - 1 else self[col_index, row_index + 1]
                    )
                if node.symbol != "|":
                    node.linked_nodes[Direction.WEST] = (
                        None if col_index == 0 else self[col_index - 1, row_index]
                    )
                    node.linked_nodes[Direction.EAST] = (
                        None if col_index == self.width - 1 else self[col_index + 1, row_index]
                    )

    def traverse(self, start_coords: tuple[int, int], start_direction: Direction) -> set[Node]:
        visited_nodes_and_directions: set[tuple[Node, Direction]] = {(self[start_coords], start_direction)}
        current_nodes_and_directions = self[start_coords].get_linked_nodes(start_direction)
        while current_nodes_and_directions:
            next_nodes_and_directions: list[tuple[Node, Direction]] = []
            for node, direction in current_nodes_and_directions:
                if (node, direction) not in visited_nodes_and_directions:
                    visited_nodes_and_directions.add((node, direction))
                    next_nodes_and_directions.extend(node.get_linked_nodes(direction))
            current_nodes_and_directions = next_nodes_and_directions
        return set(node for node, _ in visited_nodes_and_directions)

    def find_longest_traversal_path(self) -> set[Node]:
        longest_path: set[Node] = set()
        for col_index in range(self.width):
            candidate_longest_path = self.traverse((col_index, 0), Direction.SOUTH)
            if len(candidate_longest_path) > len(longest_path):
                longest_path = candidate_longest_path
            candidate_longest_path = self.traverse((col_index, self.height - 1), Direction.NORTH)
            if len(candidate_longest_path) > len(longest_path):
                longest_path = candidate_longest_path
        for row_index in range(self.height):
            candidate_longest_path = self.traverse((0, row_index), Direction.EAST)
            if len(candidate_longest_path) > len(longest_path):
                longest_path = candidate_longest_path
            candidate_longest_path = self.traverse((self.width - 1, row_index), Direction.WEST)
            if len(candidate_longest_path) > len(longest_path):
                longest_path = candidate_longest_path
        return longest_path

    @property
    def width(self) -> int:
        return len(self.nodes[0])

    @property
    def height(self) -> int:
        return len(self.nodes)
