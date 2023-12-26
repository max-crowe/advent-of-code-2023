from io import StringIO
from unittest import TestCase

from .parser import get_graph_from_input_data


class GraphTestCase(TestCase):
    def setUp(self):
        self.graph = get_graph_from_input_data(
            StringIO("""...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....""")
        )

    def test_get_shortest_distance(self):
        target_nodes = {(node.x, node.y): node for node in self.graph.target_nodes}
        distances = {
            (node.x, node.y): distance
            for node, distance in self.graph.get_shortest_distances_to_all_targets(target_nodes[(1, 5)]).items()
        }
        self.assertEqual(distances[(4, 9)], 9)
        distances = {
            (node.x, node.y): distance
            for node, distance in self.graph.get_shortest_distances_to_all_targets(target_nodes[(3, 0)]).items()
        }
        self.assertEqual(distances[(7, 8)], 15)
        distances = {
            (node.x, node.y): distance
            for node, distance in self.graph.get_shortest_distances_to_all_targets(target_nodes[(0, 2)]).items()
        }
        self.assertEqual(distances[(9, 6)], 17)

    def test_get_sum_of_distances(self):
        self.assertEqual(self.graph.get_sum_of_distances_between_all_targets(), 374)
