from io import StringIO
from unittest import TestCase

from .calculator import get_winning_products_count
from .parser import get_race_stats_from_input


class CalculatorTestCase(TestCase):
    def _calculate_brute_force(self, time: int, distance: int) -> int:
        winning_times = set()
        for i in range(time):
            charge_time = time - i
            distance_with_time = i * charge_time
            if distance_with_time > distance:
                winning_times.add(charge_time)
        return len(winning_times)

    def test_get_winning_products_count(self):
        self.assertEqual(get_winning_products_count(7, 9), 4)
        self.assertEqual(get_winning_products_count(15, 40), 8)
        self.assertEqual(get_winning_products_count(30, 200), 9)

    def test_get_winning_products_count_against_brute_force(self):
        self.assertEqual(
            get_winning_products_count(48, 261),
            self._calculate_brute_force(48, 261)
        )
        self.assertEqual(
            get_winning_products_count(93, 1192),
            self._calculate_brute_force(93, 1192)
        )
        self.assertEqual(
            get_winning_products_count(84, 1019),
            self._calculate_brute_force(84, 1019)
        )
        self.assertEqual(
            get_winning_products_count(66, 1063),
            self._calculate_brute_force(66, 1063)
        )


class ParserTestCase(TestCase):
    def test_parser(self):
        input_data = StringIO("""Time:        48     93     84     66
Distance:   261   1192   1019   1063""")
        self.assertEqual(
            get_race_stats_from_input(input_data),
            [
                (48, 261),
                (93, 1192),
                (84, 1019),
                (66, 1063),
            ]
        )
