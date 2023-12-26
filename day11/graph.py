from dataclasses import dataclass, field
from math import ceil


class Node:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.edges: dict["Node", int] = {}

    def __repr__(self):
        return f"Node({self.x}, {self.y})"

    def connect_to(self, other: "Node", weight: int):
        if other not in self.edges:
            self.edges[other] = weight
            other.edges[self] = weight


@dataclass
class Graph:
    nodes: set[Node] = field(default_factory=set)
    target_nodes: list[Node] = field(default_factory=list)

    def get_shortest_distances_to_all_targets(self, from_node: Node) -> dict[Node, int]:
        known_nodes: set[Node] = set()
        distances: dict[Node, int | None] = {
            node: 0 if node is from_node else None for node in self.nodes
        }
        while len(known_nodes) != len(self.nodes):
            test_node, distance = next(
                iter(
                    sorted(
                        [
                            (node, distance) for node, distance in distances.items()
                            if distance is not None
                            and node not in known_nodes
                        ],
                        key=lambda pair: pair[1]
                    )
                )
            )
            known_nodes.add(test_node)
            for linked_node, weight in test_node.edges.items():
                new_distance = distance + weight
                if distances[linked_node] is None or distances[linked_node] > new_distance:
                    distances[linked_node] = new_distance
        return {node: distances[node] for node in self.target_nodes if node is not from_node}

    def get_sum_of_distances_between_all_targets(self) -> int:
        pair_distances: dict[tuple[Node, Node], int] = {}
        for i, node in enumerate(self.target_nodes):
            if len([key for key in pair_distances.keys() if node in key]) < len(self.target_nodes) - 1:
                distances = self.get_shortest_distances_to_all_targets(node)
                for target_node, distance in distances.items():
                    key = [node, target_node]
                    key.sort(key=lambda node: (node.x, node.y))
                    pair_distances[(key[0], key[1])] = distance
        return sum(pair_distances.values())
