from io import StringIO
from unittest import TestCase

from .graph import Direction
from .parser import get_graph_from_input_data


class ParserTestCase(TestCase):
    def test_parser(self):
        graph = get_graph_from_input_data(StringIO("""R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)"""))
        self.assertEqual(graph.width, 7)
        self.assertEqual(graph.height, 10)
        self.assertIs(graph[0, 0].linked_nodes[Direction.EAST], graph[1, 0])
        self.assertIn(graph[0, 0], graph.edge_nodes)
        self.assertEqual(len(graph.edge_nodes), 38)
        self.assertIs(graph[0, 1].linked_nodes[Direction.NORTH], graph[0, 0])


class GraphTestCase(TestCase):
    def setUp(self):
        self.graph = get_graph_from_input_data(StringIO("""R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)"""))

    def test_get_area(self):
        self.assertEqual(self.graph.get_area(), 62)
