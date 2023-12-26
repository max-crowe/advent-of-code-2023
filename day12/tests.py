from unittest import TestCase

from .records import Condition, Record


class RecordTestCase(TestCase):
    def test_consume_contiguous_group(self):
        record = Record([Condition(c) for c in "?###????????"])
        self.assertEqual(
            record.consume_contiguous_group(0, 3),
            [
                Condition.UNKNOWN,
                Condition.BROKEN,
                Condition.BROKEN,
                Condition.BROKEN,
            ]
        )
        self.assertEqual(
            record.consume_contiguous_group(1, 3),
            [
                Condition.BROKEN,
                Condition.BROKEN,
                Condition.BROKEN,
            ]
        )
        self.assertIsNone(
            record.consume_contiguous_group(2, 3)
        )
        self.assertEqual(
            record.consume_contiguous_group(4, 3),
            [
                Condition.UNKNOWN,
                Condition.UNKNOWN,
                Condition.UNKNOWN,
            ]
        )
        record = Record([Condition(c) for c in "???.###"])
        self.assertEqual(
            record.consume_contiguous_group( 0, 1),
            [Condition.UNKNOWN]
        )
        self.assertEqual(
            record.consume_contiguous_group(3, 1),
            [Condition.UNKNOWN]
        )

