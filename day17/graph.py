import heapq
from collections import defaultdict
from copy import copy
from dataclasses import dataclass, field
from enum import Enum, auto


class Direction(Enum):
    NORTH = auto()
    EAST = auto()
    SOUTH = auto()
    WEST = auto()


@dataclass
class Node:
    x: int
    y: int
    intrinsic_weight: int
    linked_nodes: dict[Direction, "Node"] = field(default_factory=dict)

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return f"Node(({self.x}, {self.y}, {self.intrinsic_weight}))"

    def link_to(self, other: "Node", direction: Direction):
        self.linked_nodes[direction] = other


class Graph:
    def __init__(self, nodes: list[list[Node]]):
        self.nodes = nodes
        self.link_nodes()

    def __getitem__(self, coords: tuple[int, int]) -> Node:
        return self.nodes[coords[1]][coords[0]]

    def link_nodes(self):
        for row_index in range(self.height):
            for col_index in range(self.width):
                if row_index > 0:
                    self[col_index, row_index].link_to(
                        self[col_index, row_index - 1], Direction.NORTH
                    )
                if row_index < self.height - 1:
                    self[col_index, row_index].link_to(
                        self[col_index, row_index + 1], Direction.SOUTH
                    )
                if col_index > 0:
                    self[col_index, row_index].link_to(
                        self[col_index - 1, row_index], Direction.WEST
                    )
                if col_index < self.width - 1:
                    self[col_index, row_index].link_to(
                        self[col_index + 1, row_index], Direction.EAST
                    )

    @staticmethod
    def get_ideal_distance(from_node: Node, to_node: Node) -> int:
        return abs(from_node.x - to_node.x) + abs(from_node.y - to_node.y)

    def get_shortest_path(self, from_node: Node, to_node: Node, max_steps_between_pivot: int = 3) -> int:
        expandable_nodes: list[tuple[int, int, Node]] = [(0, 0, from_node)]
        heapq.heapify(expandable_nodes)
        queue_entry_count = 1
        paths: dict[Node, list[tuple[int, Direction]]] = {from_node: []}
        known_distances: defaultdict[Node, int | None] = defaultdict(lambda: None)
        known_distances[from_node] = 0

        while expandable_nodes:
            distance_to_current, _, current = heapq.heappop(expandable_nodes)
            if current is to_node:
                return sum(pair[0] for pair in paths[current])
            neighbors: dict[Direction, Node] = copy(current.linked_nodes)
            must_pivot = len(set(pair[1] for pair in paths[current][-1 * max_steps_between_pivot:])) == 1
            if must_pivot:
                try:
                    del neighbors[paths[current][-1][1]]
                except KeyError:
                    pass
            for direction, neighbor in neighbors.items():
                tentative_distance = known_distances[current] + neighbor.intrinsic_weight
                if known_distances[neighbor] is None or tentative_distance < known_distances[neighbor]:
                    paths[neighbor] = paths[current] + [(neighbor.intrinsic_weight, direction)]
                    known_distances[neighbor] = tentative_distance
                    heapq.heappush(
                        expandable_nodes,
                        (tentative_distance + self.get_ideal_distance(current, neighbor), queue_entry_count, neighbor)
                    )
                    queue_entry_count += 1
        raise RuntimeError("Goal was never reached")

    @property
    def width(self) -> int:
        return len(self.nodes[0])

    @property
    def height(self) -> int:
        return len(self.nodes)

