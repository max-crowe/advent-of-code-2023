from io import StringIO
from unittest import TestCase

from .parser import get_directions_and_map_from_input


class ParserTestCase(TestCase):
    def test_parser(self):
        input_data = StringIO("""LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)""")
        directions, map = get_directions_and_map_from_input(input_data)
        self.assertEqual(directions, "LLR")
        self.assertEqual(map.nodes, {
            "AAA": ("BBB", "BBB"),
            "BBB": ("AAA", "ZZZ"),
            "ZZZ": ("ZZZ", "ZZZ")
        })


class NavigationTestCase(TestCase):
    def test_get_step_count(self):
        directions, map = get_directions_and_map_from_input(
            StringIO("""RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)""")
        )
        self.assertEqual(
            map.get_step_count("AAA", "ZZZ", directions),
            2
        )

        directions, map = get_directions_and_map_from_input(
            StringIO("""LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)""")
        )
        self.assertEqual(
            map.get_step_count("AAA", "ZZZ", directions),
            6
        )

    def test_get_multi_step_count(self):
        directions, map = get_directions_and_map_from_input(
            StringIO("""LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)""")
        )
        self.assertEqual(
            map.get_multi_step_count("A", "Z", directions),
            6
        )
