from io import StringIO
from unittest import TestCase

from .graph import Direction
from .parser import get_graph_from_input_data


class ParserTestCase(TestCase):
    def test_parser(self):
        input_data = StringIO("""2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533""")
        graph = get_graph_from_input_data(input_data)
        self.assertEqual(graph.width, 13)
        self.assertEqual(graph.height, 13)
        self.assertNotIn(Direction.NORTH, graph[0, 0].linked_nodes)
        self.assertNotIn(Direction.WEST, graph[0, 0].linked_nodes)
        self.assertIs(graph[0, 0].linked_nodes[Direction.EAST], graph[1, 0])
        self.assertIs(graph[0, 0].linked_nodes[Direction.SOUTH], graph[0, 1])
        self.assertEqual(graph[0, 0].intrinsic_weight, 2)
        self.assertNotIn(Direction.SOUTH, graph[12, 12].linked_nodes)
        self.assertNotIn(Direction.EAST, graph[12, 12].linked_nodes)
        self.assertIs(graph[12, 12].linked_nodes[Direction.NORTH], graph[12, 11])
        self.assertIs(graph[12, 12].linked_nodes[Direction.WEST], graph[11, 12])
        self.assertEqual(graph[12, 12].intrinsic_weight, 3)
        self.assertIs(graph[6, 6].linked_nodes[Direction.NORTH], graph[6, 5])
        self.assertIs(graph[6, 6].linked_nodes[Direction.EAST], graph[7, 6])
        self.assertIs(graph[6, 6].linked_nodes[Direction.SOUTH], graph[6, 7])
        self.assertIs(graph[6, 6].linked_nodes[Direction.WEST], graph[5, 6])
        self.assertEqual(graph[6, 6].intrinsic_weight, 6)


class GraphTestCase(TestCase):
    def setUp(self):
        self.graph = get_graph_from_input_data(
            StringIO("""2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533""")
        )

    def test_get_ideal_distance(self):
        self.assertEqual(
            self.graph.get_ideal_distance(self.graph[0, 0], self.graph[12, 12]),
            24
        )
        self.assertEqual(
            self.graph.get_ideal_distance(self.graph[12, 12], self.graph[0, 0]),
            24
        )
        self.assertEqual(
            self.graph.get_ideal_distance(self.graph[6, 6], self.graph[7, 6]),
            1
        )
        self.assertEqual(
            self.graph.get_ideal_distance(self.graph[6, 7], self.graph[6, 6]),
            1
        )

    def test_get_shortest_path(self):
        self.assertEqual(
            self.graph.get_shortest_path(self.graph[0, 0], self.graph[12, 12]),
            102
        )
