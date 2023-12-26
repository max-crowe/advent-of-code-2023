from dataclasses import dataclass, field
from enum import IntEnum, auto
from functools import cached_property
from itertools import chain


class Orientation(IntEnum):
    NORTH_SOUTH = auto()
    EAST_WEST = auto()

    @property
    def complement(self) -> "Orientation":
        return Orientation.NORTH_SOUTH if self is Orientation.EAST_WEST else Orientation.EAST_WEST


class Direction(IntEnum):
    NORTH = -2
    EAST = 1
    SOUTH = 2
    WEST = -1

    @property
    def orientation(self) -> Orientation:
        return Orientation.NORTH_SOUTH if abs(self) == Direction.SOUTH else Orientation.EAST_WEST

    @property
    def complement(self) -> "Direction":
        return Direction(self * -1)


class Node:
    def __init__(self, x: int, y: int, directions: tuple[Direction, Direction]):
        self.x = x
        self.y = y
        self.directions = directions
        self.linked_nodes: dict[Direction, "Node | None"] = {}

    def __repr__(self) -> str:
        return f"Node(({self.x}, {self.y}, {self.directions}))"

    def get_next_linked_node(self, direction: Direction) -> tuple["Node", Direction]:
        return (
            self.linked_nodes[direction],
            list(filter(lambda d: d is not direction.complement, self.linked_nodes[direction].directions))[0]
        )


@dataclass
class Section:
    fill_nodes: set[tuple[int, int]] = field(default_factory=set)
    edge_nodes: set[Node] = field(default_factory=set)
    is_interior: bool = True

    def merge(self, other: "Section") -> "Section":
        if self.is_interior != other.is_interior:
            raise ValueError("Cannot merge sections unless they are both interior or exterior")
        merged = Section(is_interior=self.is_interior)
        merged.fill_nodes = self.fill_nodes | other.fill_nodes
        merged.edge_nodes = self.edge_nodes | other.edge_nodes
        return merged


class Graph:
    def __init__(self, nodes: list[list[Node | None]], start_pos: tuple[int, int]):
        self.nodes = nodes
        self.start_pos = start_pos
        self.loop_nodes: set[Node] = set()
        self.openings: set[tuple[Node, Node]] = set()
        self.opening_nodes: set[Node] = set()

    def get_next_position(self, x: int, y: int, direction: Direction) -> tuple[int, int] | None:
        match direction:
            case Direction.EAST | Direction.WEST:
                next_pos = x + (1 if direction > 0 else -1)
                if 0 <= next_pos < self.width:
                    return next_pos, y
            case Direction.NORTH | Direction.SOUTH:
                next_pos = y + (1 if direction > 0 else -1)
                if 0 <= next_pos < self.height:
                    return x, next_pos

    def get_next_node(self, x: int, y: int, direction: Direction) -> Node | None:
        pos = self.get_next_position(x, y, direction)
        if pos is not None:
            return self.nodes[pos[1]][pos[0]]

    def confirm_opening(self, node: Node, adjacent_node: Node) -> bool:
        shared_directions = list(set(node.directions) & set(adjacent_node.directions))
        if len(shared_directions) != 1:
            return False
        return self.get_next_node(
            node.x, node.y, shared_directions[0].complement
        ) is None or self.get_next_node(
            adjacent_node.x, adjacent_node.y, shared_directions[0].complement
        ) is None

    def get_next_opening_node(self, opening: tuple[Node, Node]) -> Node:
        shared_direction = list(set(opening[0].directions) & set(opening[1].directions))[0]
        current_node, current_direction = opening[0].get_next_linked_node(shared_direction)
        while current_node not in self.opening_nodes:
            current_node, current_direction = current_node.get_next_linked_node(current_direction)
        assert current_node is not opening[0]
        return current_node

    def traverse_from_start(self):
        current_node = self.start_node
        current_pos = self.start_pos
        current_direction = current_node.directions[0]
        while True:
            self.loop_nodes.add(current_node)
            if current_direction in current_node.linked_nodes:
                raise RuntimeError("Unexpected cycle detected")
            current_pos = self.get_next_position(*current_pos, current_direction)
            if current_pos is None:
                raise RuntimeError("Trail unexpectedly cold")
            next_node = self.nodes[current_pos[1]][current_pos[0]]
            if current_direction.complement not in next_node.directions:
                raise RuntimeError("Next node does not link back to this node")
            current_node.linked_nodes[current_direction] = next_node
            next_node.linked_nodes[current_direction.complement] = current_node
            current_node = next_node
            if current_node is self.start_node:
                break
            current_direction = [
                direction for direction in next_node.directions
                if direction is not current_direction.complement
            ][0]
        current_node, current_direction = self.start_node.get_next_linked_node(
            self.start_node.directions[0]
        )
        while current_node is not self.start_node:
            for direction in Direction:
                adjacent_pos = self.get_next_position(current_node.x, current_node.y, direction)
                if (
                    adjacent_pos is not None
                    and (adjacent_node := self.nodes[adjacent_pos[1]][adjacent_pos[0]])
                    and adjacent_node not in current_node.linked_nodes.values()
                    and self.confirm_opening(current_node, adjacent_node)
                ):
                    opening = [current_node, adjacent_node]
                    opening.sort(key=lambda node: (node.x, node.y))
                    self.openings.add((opening[0], opening[1]))
                    self.opening_nodes.add(opening[0])
                    self.opening_nodes.add(opening[1])
            current_node, current_direction = current_node.get_next_linked_node(
                current_direction
            )

    def get_steps_to_start(self, from_node: Node, direction: Direction) -> int:
        if direction not in from_node.linked_nodes:
            self.traverse_from_start()
        current_node, current_direction = from_node.get_next_linked_node(direction)
        step_count = 1
        while current_node is not self.start_node:
            if current_node is from_node:
                raise RuntimeError("Unexpected circular reference")
            current_node, current_direction = current_node.get_next_linked_node(
                current_direction
            )
            step_count += 1
        return step_count

    def get_steps_to_farthest_position(self) -> int:
        return self.get_steps_to_start(self.start_node, self.start_node.directions[0]) // 2

    def fill_contiguous_section(
        self,
        x: int,
        y: int,
        section: Section,
    ) -> bool:
        is_interior = x not in (0, self.width) and y not in (0, self.height)
        if (node := self.nodes[y][x]) and node in self.loop_nodes:
            directions = node.directions
            section.edge_nodes.add(node)
        else:
            section.fill_nodes.add((x, y))
            directions = list(Direction)
        for direction in directions:
            adjacent_pos = self.get_next_position(x, y, direction)
            adjacent_node = None if adjacent_pos is None else self.nodes[adjacent_pos[1]][adjacent_pos[0]]
            if (
                adjacent_pos is None
                or adjacent_pos in section.fill_nodes
                or adjacent_node in section.edge_nodes
            ):
                continue
            is_interior = self.fill_contiguous_section(
                adjacent_pos[0], adjacent_pos[1], section
            ) and is_interior
        return is_interior

    def get_contiguous_sections(self) -> list[Section]:
        edge_positions = {(node.x, node.y) for node in self.loop_nodes}
        unvisited_positions: set[tuple[int, int]] = set()
        unknown_sections: list[Section] = []
        exterior_section = Section(is_interior=False)
        self.fill_contiguous_section(0, 0, exterior_section)
        for x_index in range(self.width):
            for y_index in range(self.height):
                if (
                    (x_index, y_index) not in exterior_section.fill_nodes
                    and (x_index, y_index) not in edge_positions
                ):
                    unvisited_positions.add((x_index, y_index))
        while unvisited_positions:
            section = Section()
            unknown_sections.append(section)
            position = unvisited_positions.pop()
            section.is_interior = self.fill_contiguous_section(position[0], position[1], section)
            unvisited_positions -= section.fill_nodes
        combined_sections: list[Section] = []
        for section in unknown_sections:
            exterior_section = exterior_section.merge(section)
        return combined_sections


    @cached_property
    def width(self) -> int:
        return len(self.nodes[0])

    @cached_property
    def height(self) -> int:
        return len(self.nodes)

    @cached_property
    def start_node(self) -> Node:
        start_node_directions: list[Direction] = []
        adjacent_nodes: list[Node | None] = [None, None, None, None]
        if self.start_pos[1]:
            adjacent_nodes[0] = self.nodes[self.start_pos[1] - 1][self.start_pos[0]]
        if self.start_pos[0] < self.width - 1:
            adjacent_nodes[1] = self.nodes[self.start_pos[1]][self.start_pos[0] + 1]
        if self.start_pos[1] < self.height - 1:
            adjacent_nodes[2] = self.nodes[self.start_pos[1] + 1][self.start_pos[0]]
        if self.start_pos[0]:
            adjacent_nodes[3] = self.nodes[self.start_pos[1]][self.start_pos[0] - 1]
        if adjacent_nodes[0] and Direction.SOUTH in adjacent_nodes[0].directions:
            start_node_directions.append(Direction.NORTH)
        if adjacent_nodes[1] and Direction.WEST in adjacent_nodes[1].directions:
            start_node_directions.append(Direction.EAST)
        if adjacent_nodes[2] and Direction.NORTH in adjacent_nodes[2].directions:
            start_node_directions.append(Direction.SOUTH)
        if adjacent_nodes[3] and Direction.EAST in adjacent_nodes[3].directions:
            start_node_directions.append(Direction.WEST)
        assert len(start_node_directions) == 2
        start_node = Node(
            self.start_pos[0],
            self.start_pos[1],
            (start_node_directions[0], start_node_directions[1])
        )
        self.nodes[self.start_pos[1]][self.start_pos[0]] = start_node
        return start_node
