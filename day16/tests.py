from io import StringIO
from unittest import TestCase

from .graph import Direction, Node, NodeType
from .parser import get_graph_from_input_data


class ParserTestCase(TestCase):
    def test_parser(self):
        graph = get_graph_from_input_data(StringIO(""".|...\\....
|.-.\\.....
.....|-...
........|.
..........
.........\\
..../.\\\\..
.-.-/..|..
.|....-|.\\
..//.|...."""))
        self.assertEqual(graph.width, 10)
        self.assertEqual(graph.height, 10)
        self.assertIs(graph[0, 1].type, NodeType.SPLITTER)
        self.assertEqual(graph[0, 1].symbol, "|")
        self.assertNotIn(Direction.EAST, graph[0, 1].linked_nodes)
        self.assertNotIn(Direction.WEST, graph[0, 1].linked_nodes)
        self.assertEqual(graph[0, 1].linked_nodes[Direction.NORTH].type, NodeType.EMPTY)
        self.assertEqual(graph[0, 1].linked_nodes[Direction.SOUTH].type, NodeType.EMPTY)
        self.assertIs(graph[5, 0].type, NodeType.MIRROR)
        self.assertEqual(graph[5, 0].symbol, "\\")
        self.assertIsNone(graph[5, 0].linked_nodes[Direction.NORTH])
        self.assertIsInstance(graph[5, 0].linked_nodes[Direction.EAST], Node)
        self.assertIsInstance(graph[5, 0].linked_nodes[Direction.WEST], Node)
        self.assertIsInstance(graph[5, 0].linked_nodes[Direction.SOUTH], Node)


class GraphTestCase(TestCase):
    def setUp(self):
        self.graph = get_graph_from_input_data(StringIO(""".|...\\....
|.-.\\.....
.....|-...
........|.
..........
.........\\
..../.\\\\..
.-.-/..|..
.|....-|.\\
..//.|...."""))

    def test_get_linked_nodes(self):
        self.assertEqual(
            self.graph[0, 0].get_linked_nodes(Direction.EAST),
            [(self.graph[1, 0], Direction.EAST)]
        )
        self.assertEqual(
            self.graph[1, 0].get_linked_nodes(Direction.EAST),
            [(self.graph[1, 1], Direction.SOUTH)]
        )
        self.assertCountEqual(
            self.graph[2, 1].get_linked_nodes(Direction.SOUTH),
            [
                (self.graph[1, 1], Direction.WEST),
                (self.graph[3, 1], Direction.EAST)
            ]
        )
        self.assertEqual(
            self.graph[5, 0].get_linked_nodes(Direction.EAST),
            [(self.graph[5, 1], Direction.SOUTH)]
        )
        self.assertEqual(
            self.graph[5, 0].get_linked_nodes(Direction.WEST),
            []
        )
        self.assertEqual(
            self.graph[5, 0].get_linked_nodes(Direction.SOUTH),
            [(self.graph[6, 0], Direction.EAST)]
        )
        self.assertEqual(
            self.graph[5, 0].get_linked_nodes(Direction.NORTH),
            [(self.graph[4, 0], Direction.WEST)]
        )

    def test_traverse(self):
        visited_nodes = self.graph.traverse((0, 0), Direction.EAST)
        self.assertEqual(len(visited_nodes), 46)

    def test_find_longest_traversal_path(self):
        longest_path = self.graph.find_longest_traversal_path()
        self.assertEqual(len(longest_path), 51)
