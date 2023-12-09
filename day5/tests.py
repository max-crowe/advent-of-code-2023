from io import StringIO
from unittest import TestCase

from .mapping import RangeSet, RangeSetOrchestrator, find_range_index, get_intersections
from .parser import get_seeds_and_orchestrator_from_input, get_seed_ranges_and_orchestrator_from_input


class RangeUtilsTestCase(TestCase):
    def test_get_intersections(self):
        source = [
            range(3, 6),
            range(0, 2),
            range(30, 33),
            range(9, 15),
        ]
        target = [
            range(20, 25),
            range(1, 5),
            range(10, 20),
            range(5, 9)
        ]
        self.assertCountEqual(
            get_intersections(source, target),
            [
                range(3, 5),
                range(5, 6),
                range(1, 2),
                range(10, 15),
            ]
        )
        target = [
            range(0, 33)
        ]
        self.assertCountEqual(
            get_intersections(source, target),
            source
        )
        target = [
            range(30, 31)
        ]
        self.assertCountEqual(
            get_intersections(source, target),
            target
        )

    def test_find_range_index(self):
        ranges = [
            range(2, 29),
            range(23, 41),
            range(0, 1)
        ]
        self.assertEqual(find_range_index(10, ranges), 0)
        self.assertEqual(find_range_index(25, ranges), 0)
        self.assertEqual(find_range_index(29, ranges), 1)
        self.assertEqual(find_range_index(2, ranges), 0)
        self.assertEqual(find_range_index(0, ranges), 2)
        with self.assertRaises(ValueError):
            find_range_index(1, ranges)
        with self.assertRaises(ValueError):
            find_range_index(41, ranges)



class RangeSetTestCase(TestCase):
    def test_get_mapped_value(self):
        range_set = RangeSet("foo", "bar")
        range_set.add_range(50, 98, 2)
        range_set.add_range(52, 50, 48)
        self.assertEqual(range_set.get_mapped_value(98), 50)
        self.assertEqual(range_set.get_mapped_value(99), 51)
        self.assertEqual(range_set.get_mapped_value(53), 55)
        self.assertEqual(range_set.get_mapped_value(10), 10)
        self.assertEqual(range_set.get_mapped_value(50, reverse=True), 98)
        self.assertEqual(range_set.get_mapped_value(51, reverse=True), 99)
        self.assertEqual(range_set.get_mapped_value(55, reverse=True), 53)
        self.assertEqual(range_set.get_mapped_value(10, reverse=True), 10)

    def test_sorted_destination_range_indices(self):
        range_set = RangeSet("foo", "bar")
        range_set.add_range(52, 50, 48)
        range_set.add_range(50, 98, 2)
        self.assertEqual(range_set.sorted_destination_range_indices, [1, 0])


class RangeSetOrchestratorTestCase(TestCase):
    def setUp(self):
        self.orchestrator = RangeSetOrchestrator()
        for source, destination, values in (
            ("seed", "soil", ((50, 98, 2), (52, 50, 48))),
            ("soil", "fertilizer", ((0, 15, 37), (37, 52, 2), (39, 0, 15))),
            ("fertilizer", "water", ((49, 53, 8), (0, 11, 42), (42, 0, 7), (57, 7, 4))),
            ("water", "light", ((88, 18, 7), (18, 25, 70))),
            ("light", "temperature", ((45, 77, 23), (81, 45, 19), (68, 64, 13))),
            ("temperature", "humidity", ((0, 69, 1), (1, 0, 69))),
            ("humidity", "location", ((60, 56, 37), (56, 93, 4)))
        ):
            range_set = RangeSet(source, destination)
            self.orchestrator.add_range_set(range_set)
            for dest_start, source_start, length in values:
                range_set.add_range(dest_start, source_start, length)

    def test_get_mapped_value(self):
        self.assertEqual(
            self.orchestrator.get_mapped_value(79, "seed"),
            82
        )
        self.assertEqual(
            self.orchestrator.get_mapped_value(14, "seed"),
            43
        )
        self.assertEqual(
            self.orchestrator.get_mapped_value(55, "seed"),
            86
        )
        self.assertEqual(
            self.orchestrator.get_mapped_value(13, "seed"),
            35
        )

    def test_get_reverse_mapped_value(self):
        self.assertEqual(
            self.orchestrator.get_reverse_mapped_value(82, "location"),
            79
        )
        self.assertEqual(
            self.orchestrator.get_reverse_mapped_value(43, "location"),
            14
        )
        self.assertEqual(
            self.orchestrator.get_reverse_mapped_value(86, "location"),
            55
        )
        self.assertEqual(
            self.orchestrator.get_reverse_mapped_value(35, "location"),
            13
        )
        ranges = [range(79, 79 + 14), range(55, 55 + 13)]
        limit = self.orchestrator.lookup_table_by_destination["location"].destination_ranges[
            self.orchestrator.lookup_table_by_destination["location"].sorted_destination_range_indices[-1]
        ].stop
        for location_id in range(0, limit):
            seed_value = self.orchestrator.get_reverse_mapped_value(
                location_id, "location"
            )
            try:
                find_range_index(seed_value, ranges)
            except ValueError:
                pass
            else:
                self.assertEqual(location_id, 46)
                break



class ParserTestCase(TestCase):
    def test_parser(self):
        input_data = StringIO("""seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4""")
        seeds, orchestrator = get_seeds_and_orchestrator_from_input(input_data)
        self.assertEqual(seeds, [79, 14, 55, 13])
        self.assertEqual(
            orchestrator.get_mapped_value(13, "seed"),
            35
        )

    def test_parser_as_range(self):
        input_data = StringIO("""seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48""")
        ranges, _ = get_seed_ranges_and_orchestrator_from_input(input_data)
        self.assertEqual(
            ranges,
            [
                range(79, 79 + 14),
                range(55, 55 + 13),
            ]
        )
