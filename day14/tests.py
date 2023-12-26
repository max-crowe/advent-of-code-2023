from copy import deepcopy
from io import StringIO
from unittest import TestCase

from .maps import Map, ObstacleType
from .parser import get_map_from_input_data


class ParserTestCase(TestCase):
    def test_get_map_from_input_data(self):
        map_data = StringIO("""O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....""")
        map = get_map_from_input_data(map_data)
        self.assertEqual(map.width, 10)
        self.assertEqual(map.height, 10)
        self.assertEqual(
            map.data[0],
            [
                ObstacleType.MOBILE,
                None,
                None,
                None,
                None,
                ObstacleType.IMMOBILE,
                None,
                None,
                None,
                None,
            ]
        )
        self.assertEqual(
            map.data[-1],
            [
                ObstacleType.IMMOBILE,
                ObstacleType.MOBILE,
                ObstacleType.MOBILE,
                None,
                None,
                ObstacleType.IMMOBILE,
                None,
                None,
                None,
                None,
            ]
        )


class MapTestCase(TestCase):
    def test_shift_obstacles(self):
        map_data = StringIO("""O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....""")
        map = get_map_from_input_data(map_data)
        map.shift_obstacles()
        self.assertEqual(
            map,
            get_map_from_input_data(StringIO("""OOOO.#.O..
OO..#....#
OO..O##..O
O..#.OO...
........#.
..#....#.#
..O..#.O.O
..O.......
#....###..
#....#...."""))
        )

    def test_run_cycle(self):
        map_data = StringIO("""O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....""")
        map = get_map_from_input_data(map_data)
        map.run_cycle()
        self.assertEqual(
            map,
            get_map_from_input_data(StringIO(""".....#....
....#...O#
...OO##...
.OO#......
.....OOO#.
.O#...O#.#
....O#....
......OOOO
#...O###..
#..OO#...."""))
        )
        map.run_cycle()
        self.assertEqual(
            map,
            get_map_from_input_data(StringIO(""".....#....
....#...O#
.....##...
..O#......
.....OOO#.
.O#...O#.#
....O#...O
.......OOO
#..OO###..
#.OOO#...O"""))
        )
        map.run_cycle()
        self.assertEqual(
            map,
            get_map_from_input_data(StringIO(""".....#....
....#...O#
.....##...
..O#......
.....OOO#.
.O#...O#.#
....O#...O
.......OOO
#...O###.O
#.OOO#...O"""))
        )

    def test_run_cycles(self):
        map_data = StringIO("""O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....""")
        map = get_map_from_input_data(map_data)
        map2 = deepcopy(map)
        for _ in range(49):
            map.run_cycle()
        expected_load = map.get_total_load()
        map2.run_cycles(49)
        self.assertEqual(map2.get_total_load(), expected_load)

    def test_calculate_load(self):
        map = get_map_from_input_data(StringIO("""OOOO.#.O..
OO..#....#
OO..O##..O
O..#.OO...
........#.
..#....#.#
..O..#.O.O
..O.......
#....###..
#....#...."""))
        self.assertEqual(map.get_total_load(), 136)
