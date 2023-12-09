from io import StringIO
from unittest import TestCase

from .parser import iter_sequences_from_input
from .predictor import extrapolate, reduce_sequence


class PredictorTestCase(TestCase):
    def test_reduce_sequence(self):
        self.assertEqual(
            list(reduce_sequence([1, 3, 6, 10, 15, 21])),
            [(1, 21), (2, 6), (1, 1)]
        )
        self.assertEqual(
            list(reduce_sequence([10, 13, 16, 21, 30, 45])),
            [(10, 45), (3, 15), (0, 6), (2, 2)]
        )
        self.assertEqual(
            list(reduce_sequence([0, 3, 6, 9, 12, 15])),
            [(0, 15), (3, 3)]
        )
        self.assertEqual(
            list(reduce_sequence([8, 6, 4, 2, 0, -3, -9])),
            [(8, -9), (-2, -6), (0, -3), (0, -2), (0, -1), (-1, 0), (1, 1)],
        )

    def test_extrapolate(self):
        self.assertEqual(extrapolate([1, 3, 6, 10, 15, 21]), 28)
        self.assertEqual(extrapolate([10, 13, 16, 21, 30, 45]), 68)
        self.assertEqual(extrapolate([0, 3, 6, 9, 12, 15]), 18)

    def test_extrapolate_left(self):
        self.assertEqual(extrapolate([10, 13, 16, 21, 30, 45], True), 5)
        self.assertEqual(extrapolate([1, 3, 6, 10, 15, 21], True), 0)
        self.assertEqual(extrapolate([0, 3, 6, 9, 12, 15], True), -3)


class ParserTestCase(TestCase):
    def test_parser(self):
        input = StringIO("""0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45""")
        sequences = list(iter_sequences_from_input(input))
        self.assertEqual(
            sequences,
            [
                [0, 3, 6, 9, 12, 15],
                [1, 3, 6, 10, 15, 21],
                [10, 13, 16, 21, 30, 45]
            ]
        )
        self.assertEqual(sum(extrapolate(seq) for seq in sequences), 114)

