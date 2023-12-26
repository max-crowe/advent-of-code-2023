from io import StringIO
from unittest import TestCase

from .maps import Map, Orientation, TerrainType
from .parser import iter_maps_from_input


class MapTestCase(TestCase):
    def test_item_access(self):
        map_data = """##..##..##.
######..###
.####.##.##
..........#
.####.##.##
.####....##
..##..##..#"""
        map = Map([[TerrainType(c) for c in line.strip()] for line in StringIO(map_data)])
        self.assertIs(map[0, 0], TerrainType.ROCK)
        self.assertIs(map[0, 2], TerrainType.ASH)
        self.assertIs(map[10, 0], TerrainType.ASH)
        self.assertIs(map[10, 6], TerrainType.ROCK)

    def test_dimensions(self):
        map_data = """##.##.#.#..##
##.##.#.#...#
.#.###......#
.###.##..#..#
##.#.##....##
.#..###.###.#
.#...#...#.##
#.#.##.#...##
#.###.#.##.#.
#.#.#...####.
#.#.#...####.
#.###.#.##.#.
#.#.##.#...##
#####..#..##."""
        map = Map([[TerrainType(c) for c in line.strip()] for line in StringIO(map_data)])
        self.assertEqual(map.width, 13)
        self.assertEqual(map.height, 14)

    def test_offset_in_bounds(self):
        map_data = """##..##..##.
######..###
.####.##.##
..........#
.####.##.##
.####....##
..##..##..#"""
        map = Map([[TerrainType(c) for c in line.strip()] for line in StringIO(map_data)])
        self.assertTrue(map.offset_in_bounds(3, 1, Orientation.VERTICAL))
        self.assertTrue(map.offset_in_bounds(3, 3, Orientation.VERTICAL))
        self.assertFalse(map.offset_in_bounds(3, 4, Orientation.VERTICAL))
        self.assertFalse(map.offset_in_bounds(4, 3, Orientation.VERTICAL))
        self.assertFalse(map.offset_in_bounds(1, 3, Orientation.VERTICAL))
        self.assertTrue(map.offset_in_bounds(4, 5, Orientation.HORIZONTAL))
        self.assertFalse(map.offset_in_bounds(6, 5, Orientation.HORIZONTAL))

        map_data = """.........#.##
...........##
..###....##..
##.##.#..#..#
####....####.
##.####.#####
....##.#.....
##.#..##..#.#
###...##.....
##..##..###..
......######.
###.##.#####.
...#.##.#####
##..#..#.##.#
#####..#..##."""
        map = Map([[TerrainType(c) for c in line.strip()] for line in StringIO(map_data)])
        self.assertTrue(map.offset_in_bounds(1, 1, Orientation.HORIZONTAL))
        self.assertTrue(map.offset_in_bounds(11, 1, Orientation.HORIZONTAL))

    def test_is_reflection(self):
        map_data = """##..##..##.
######..###
.####.##.##
..........#
.####.##.##
.####....##
..##..##..#"""
        map = Map([[TerrainType(c) for c in line.strip()] for line in StringIO(map_data)])
        self.assertFalse(map.is_reflection(6, Orientation.HORIZONTAL))
        self.assertTrue(map.is_reflection(2, Orientation.HORIZONTAL))
        self.assertFalse(map.is_reflection(2, Orientation.HORIZONTAL, 1))

        map_data = """#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""
        map = Map([[TerrainType(c) for c in line.strip()] for line in StringIO(map_data)])
        self.assertTrue(map.is_reflection(3, Orientation.VERTICAL))
        self.assertFalse(map.is_reflection(4, Orientation.VERTICAL))

        map_data = """.........#.##
...........##
..###....##..
##.##.#..#..#
####....####.
##.####.#####
....##.#.....
##.#..##..#.#
###...##.....
##..##..###..
......######.
###.##.#####.
...#.##.#####
##..#..#.##.#
#####..#..##."""
        map = Map([[TerrainType(c) for c in line.strip()] for line in StringIO(map_data)])
        self.assertTrue(map.is_reflection(0, Orientation.HORIZONTAL))

        map_data = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#."""
        map = Map([[TerrainType(c) for c in line.strip()] for line in StringIO(map_data)])
        self.assertFalse(map.is_reflection(4, Orientation.HORIZONTAL, 1))
        self.assertTrue(map.is_reflection(2, Orientation.VERTICAL, 1))

        map_data = """#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""
        map = Map([[TerrainType(c) for c in line.strip()] for line in StringIO(map_data)])
        self.assertFalse(map.is_reflection(3, Orientation.VERTICAL, 1))
        self.assertTrue(map.is_reflection(0, Orientation.VERTICAL, 1))

    def test_find_axis_of_reflection(self):
        map_data = """##..##..##.
######..###
.####.##.##
..........#
.####.##.##
.####....##
..##..##..#"""
        map = Map([[TerrainType(c) for c in line.strip()] for line in StringIO(map_data)])
        self.assertEqual(map.find_axis_of_reflection(), (Orientation.HORIZONTAL, 2))

        map_data = """#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""
        map = Map([[TerrainType(c) for c in line.strip()] for line in StringIO(map_data)])
        self.assertEqual(map.find_axis_of_reflection(), (Orientation.VERTICAL, 3))

        map_data = """.#....########...
.##.....####.....
.##.....####.....
##....########...
..#..##..##..##..
####.###.##.###.#
#.######....#####
..#.#...####...#.
....##.#.##.#.##.
#.#...##.##.##...
.#.##..##..##..##
#.##.#.#.##.#.#.#
.#.#....#..#....#
.#...###.##.###..
##.###........###"""
        map = Map([[TerrainType(c) for c in line.strip()] for line in StringIO(map_data)])
        self.assertEqual(map.find_axis_of_reflection(), (Orientation.HORIZONTAL, 9))

        map_data = """.........#.##
...........##
..###....##..
##.##.#..#..#
####....####.
##.####.#####
....##.#.....
##.#..##..#.#
###...##.....
##..##..###..
......######.
###.##.#####.
...#.##.#####
##..#..#.##.#
#####..#..##."""
        map = Map([[TerrainType(c) for c in line.strip()] for line in StringIO(map_data)])
        self.assertEqual(map.find_axis_of_reflection(), (Orientation.HORIZONTAL, 0))

        map_data = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#."""
        map = Map([[TerrainType(c) for c in line.strip()] for line in StringIO(map_data)])
        self.assertEqual(map.find_axis_of_reflection(1), (Orientation.VERTICAL, 2))

        map_data = """#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""
        map = Map([[TerrainType(c) for c in line.strip()] for line in StringIO(map_data)])
        self.assertTrue(map.find_axis_of_reflection(1), (Orientation.VERTICAL, 0))


class ParserTestCase(TestCase):
    def test_parser(self):
        input_data = StringIO("""##..##..##.
######..###
.####.##.##
..........#
.####.##.##
.####....##
..##..##..#

##.##.#.#..##
##.##.#.#...#
.#.###......#
.###.##..#..#
##.#.##....##
.#..###.###.#
.#...#...#.##
#.#.##.#...##
#.###.#.##.#.
#.#.#...####.
#.#.#...####.
#.###.#.##.#.
#.#.##.#...##

.........#.##
...........##
..###....##..
##.##.#..#..#
####....####.
##.####.#####
....##.#.....
##.#..##..#.#
###...##.....
##..##..###..
......######.
###.##.#####.
...#.##.#####
##..#..#.##.#
#####..#..##.""")
        maps = list(iter_maps_from_input(input_data))
        self.assertEqual(len(maps), 3)
        self.assertEqual(maps[0].width, 11)
        self.assertEqual(maps[0].height, 7)
        self.assertEqual(maps[1].width, 13)
        self.assertEqual(maps[1].height, 13)
        self.assertEqual(maps[2].width, 13)
        self.assertEqual(maps[2].height, 15)
