from io import StringIO
from unittest import TestCase

from .graph import Direction, Orientation, Section
from .parser import get_graph_from_input_data


class DirectionTestCase(TestCase):
    def test_complement(self):
        self.assertIs(Direction.NORTH.complement, Direction.SOUTH)
        self.assertIs(Direction.SOUTH.complement, Direction.NORTH)
        self.assertIs(Direction.EAST.complement, Direction.WEST)
        self.assertIs(Direction.WEST.complement, Direction.EAST)

    def test_orientation(self):
        self.assertIs(Direction.NORTH.orientation, Orientation.NORTH_SOUTH)
        self.assertIs(Direction.WEST.orientation, Orientation.EAST_WEST)


class ParserTestCase(TestCase):
    def test_get_graph_from_input(self):
        input_data = StringIO(""".....
.S-7.
.|.|.
.L-J.
.....""")
        graph = get_graph_from_input_data(input_data)
        self.assertEqual(len(graph.nodes), 5)
        self.assertEqual(len(graph.nodes[0]), 5)
        self.assertCountEqual(graph.start_node.directions, (Direction.EAST, Direction.SOUTH))

        input_data = StringIO("""-L|F7
7S-7|
L|7||
-L-J|
L|-JF
""")
        graph = get_graph_from_input_data(input_data)
        self.assertEqual(len(graph.nodes), 5)
        self.assertEqual(len(graph.nodes[0]), 5)
        self.assertCountEqual(graph.start_node.directions, (Direction.EAST, Direction.SOUTH))

        input_data = StringIO("""7-F7-
-FJ|7
SJLL7
|F--J
LJ.LJ""")
        graph = get_graph_from_input_data(input_data)
        self.assertEqual(len(graph.nodes), 5)
        self.assertEqual(len(graph.nodes[0]), 5)
        self.assertCountEqual(graph.start_node.directions, (Direction.EAST, Direction.SOUTH))

        input_data = StringIO("""7-F7-
-FJ|-
.JLLS
|F--J
..|.|
LJ.LJ""")
        graph = get_graph_from_input_data(input_data)
        self.assertEqual(len(graph.nodes), 6)
        self.assertEqual(len(graph.nodes[0]), 5)
        self.assertCountEqual(graph.start_node.directions, (Direction.WEST, Direction.SOUTH))


class GraphTestCase(TestCase):
    def test_get_steps_to_start(self):
        input_data = StringIO("""-L|F7
7S-7|
L|7||
-L-J|
L|-JF""")
        graph = get_graph_from_input_data(input_data)
        self.assertEqual(
            graph.get_steps_to_start(graph.nodes[3][3], Direction.WEST), 4
        )
        self.assertEqual(
            graph.get_steps_to_start(graph.nodes[3][2], Direction.WEST), 3
        )
        self.assertEqual(
            graph.get_steps_to_start(graph.nodes[2][3], Direction.NORTH), 3
        )
        input_data = StringIO("""7-F7-
-FJ|7
SJLL7
|F--J
LJ.LJ""")
        graph = get_graph_from_input_data(input_data)
        self.assertEqual(
            graph.get_steps_to_start(graph.nodes[4][1], Direction.WEST), 3
        )
        self.assertEqual(
            graph.get_steps_to_start(graph.nodes[2][1], Direction.NORTH), 15
        )

    def test_get_steps_to_farthest_position(self):
        input_data = StringIO("""-L|F7
7S-7|
L|7||
-L-J|
L|-JF""")
        graph = get_graph_from_input_data(input_data)
        self.assertEqual(graph.get_steps_to_farthest_position(), 4)
        input_data = StringIO("""7-F7-
-FJ|7
SJLL7
|F--J
LJ.LJ""")
        graph = get_graph_from_input_data(input_data)
        self.assertEqual(graph.get_steps_to_farthest_position(), 8)

    def test_loop_node_tracking(self):
        input_data = StringIO("""-L|F7
7S-7|
L|7||
-L-J|
L|-JF""")
        graph = get_graph_from_input_data(input_data)
        graph.traverse_from_start()
        self.assertEqual(len(graph.loop_nodes), 8)

    def test_detect_openings(self):
        input_data = StringIO("""...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........""")
        graph = get_graph_from_input_data(input_data)
        graph.traverse_from_start()
        self.assertTrue(
            graph.confirm_opening(graph.nodes[5][1], graph.nodes[5][2])
        )
        self.assertEqual(
            graph.get_next_opening_node((graph.nodes[5][1], graph.nodes[5][2])),
            graph.nodes[5][9]
        )
        self.assertFalse(
            graph.confirm_opening(graph.nodes[1][2], graph.nodes[2][2])
        )
        opening_coords = [((node_a.x, node_a.y), (node_b.x, node_b.y)) for node_a, node_b in graph.openings]
        self.assertCountEqual(
            [
                ((1, 5), (2, 5)),
                ((8, 5), (9, 5))
            ],
            opening_coords,
        )

        input_data = StringIO("""..........
.S------7.
.|F----7|.
.||....||.
.||....||.
.|L-7F-J|.
.|..||..|.
.L--JL--J.
..........""")
        graph = get_graph_from_input_data(input_data)
        graph.traverse_from_start()
        opening_coords = [((node_a.x, node_a.y), (node_b.x, node_b.y)) for node_a, node_b in graph.openings]
        self.assertCountEqual(
            [
                ((1, 5), (2, 5)),
                ((7, 5), (8, 5)),
                ((4, 5), (5, 5)),
                ((4, 7), (5, 7))
            ],
            opening_coords,
        )


    def test_fill_contiguous_section(self):
        input_data = StringIO("""-L|F7
7S-7|
L|7||
-L-J|
L|-JF""")
        graph = get_graph_from_input_data(input_data)
        graph.traverse_from_start()
        section = Section()
        self.assertFalse(graph.fill_contiguous_section(0, 0, section))
        self.assertEqual(len(section.fill_nodes), 16)

        input_data = StringIO("""...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........""")
        graph = get_graph_from_input_data(input_data)
        graph.traverse_from_start()
        section = Section()
        self.assertFalse(graph.fill_contiguous_section(0, 0, section))
        self.assertEqual(len(section.fill_nodes), 49)
        section = Section()
        self.assertTrue(graph.fill_contiguous_section(2, 6, section))
        self.assertEqual(len(section.fill_nodes), 2)
        input_data = StringIO("""..........
.S------7.
.|F----7|.
.||....||.
.||....||.
.|L-7F-J|.
.|..||..|.
.L--JL--J.
..........""")
        graph = get_graph_from_input_data(input_data)
        graph.traverse_from_start()
        section = Section()
        self.assertFalse(graph.fill_contiguous_section(0, 0, section))
        self.assertEqual(len(section.fill_nodes), 34)
