from io import StringIO
from unittest import TestCase

from .cards import Card, Hand, HandCollection, FaceCard, HandType, jokers_wild
from .parser import get_hand_collection_from_input


class CardTestCase(TestCase):
    def test_comparison(self):
        self.assertEqual(Card(2), Card(2))
        self.assertLessEqual(Card(2), Card(2))
        self.assertLessEqual(Card(2), Card(3))
        self.assertLess(Card(3), Card(FaceCard.J))
        self.assertGreater(Card(FaceCard.A), Card(FaceCard.K))

    def test_comparison_when_jokers_wild(self):
        self.assertGreater(Card(FaceCard.J), Card(FaceCard.T))
        with jokers_wild():
            self.assertLess(Card(FaceCard.J), Card(2))


class HandTestCase(TestCase):
    def test_hand_type(self):
        self.assertIs(
            Hand(1, Card(5), Card(5), Card(5), Card(5), Card(5)).type,
            HandType.FIVE_OF_A_KIND
        )
        self.assertIs(
            Hand(1, Card(5), Card(FaceCard.Q), Card(5), Card(5), Card(5)).type,
            HandType.FOUR_OF_A_KIND
        )
        self.assertIs(
            Hand(1, Card(FaceCard.T), Card(5), Card(FaceCard.T), Card(FaceCard.T), Card(5)).type,
            HandType.FULL_HOUSE
        )
        self.assertIs(
            Hand(1, Card(FaceCard.T), Card(5), Card(FaceCard.T), Card(FaceCard.T), Card(FaceCard.Q)).type,
            HandType.THREE_OF_A_KIND
        )
        self.assertIs(
            Hand(1, Card(FaceCard.T), Card(5), Card(3), Card(FaceCard.T), Card(5)).type,
            HandType.TWO_PAIR
        )
        self.assertIs(
            Hand(1, Card(FaceCard.T), Card(5), Card(3), Card(9), Card(5)).type,
            HandType.ONE_PAIR
        )
        self.assertIs(
            Hand(1, Card(FaceCard.T), Card(FaceCard.K), Card(FaceCard.Q), Card(2), Card(5)).type,
            HandType.HIGH_CARD
        )

    def test_hand_type_when_jokers_wild(self):
        with jokers_wild():
            self.assertIs(
                Hand(1, Card(FaceCard.T), Card(5), Card(FaceCard.T), Card(FaceCard.T), Card(FaceCard.J)).type,
                HandType.FOUR_OF_A_KIND
            )
            self.assertIs(
                Hand(1, Card(2), Card(FaceCard.J), Card(FaceCard.J), Card(FaceCard.J), Card(FaceCard.J)).type,
                HandType.FIVE_OF_A_KIND
            )
            self.assertIs(
                Hand(1, Card(FaceCard.J), Card(FaceCard.J), Card(FaceCard.J), Card(FaceCard.J), Card(FaceCard.J)).type,
                HandType.FIVE_OF_A_KIND
            )

    def test_comparison_when_types_differ(self):
        self.assertGreater(
            Hand(1, Card(FaceCard.T), Card(5), Card(FaceCard.T), Card(FaceCard.T), Card(FaceCard.Q)),
            Hand(1, Card(FaceCard.T), Card(5), Card(3), Card(FaceCard.T), Card(5)),
        )
        self.assertGreater(
            Hand(1, Card(FaceCard.T), Card(5), Card(3), Card(9), Card(5)),
            Hand(1, Card(FaceCard.T), Card(FaceCard.K), Card(FaceCard.Q), Card(2), Card(5)),
        )

    def test_comparison_when_types_differ_and_jokers_wild(self):
        with jokers_wild():
            self.assertGreater(
                Hand(1, Card(FaceCard.J), Card(5), Card(3), Card(FaceCard.J), Card(5)),
                Hand(1, Card(FaceCard.T), Card(5), Card(FaceCard.T), Card(FaceCard.T), Card(FaceCard.Q)),
            )

    def test_comparison_when_types_match(self):
        self.assertGreater(
            Hand(1, Card(FaceCard.T), Card(5), Card(FaceCard.T), Card(FaceCard.T), Card(FaceCard.Q)),
            Hand(1, Card(7), Card(5), Card(7), Card(7), Card(FaceCard.Q)),
        )
        self.assertGreater(
            Hand(1, Card(6), Card(7), Card(8), Card(9), Card(FaceCard.Q)),
            Hand(1, Card(6), Card(7), Card(8), Card(9), Card(FaceCard.J)),
        )

    def test_comparison_when_types_match_and_jokers_wild(self):
        with jokers_wild():
            self.assertGreater(
                Hand(1, Card(7), Card(5), Card(7), Card(7), Card(FaceCard.Q)),
                Hand(1, Card(FaceCard.J), Card(5), Card(FaceCard.T), Card(FaceCard.T), Card(FaceCard.Q)),
            )


class HandCollectionTestCase(TestCase):
    def test_value_calculation(self):
        collection = HandCollection(
            Hand(765, Card(3), Card(2), Card(FaceCard.T), Card(3), Card(FaceCard.K)),
            Hand(684, Card(FaceCard.T), Card(5), Card(5), Card(FaceCard.J), Card(5)),
            Hand(28, Card(FaceCard.K), Card(FaceCard.K), Card(6), Card(7), Card(7)),
            Hand(220, Card(FaceCard.K), Card(FaceCard.T), Card(FaceCard.J), Card(FaceCard.J), Card(FaceCard.T)),
            Hand(483, Card(FaceCard.Q), Card(FaceCard.Q), Card(FaceCard.Q), Card(FaceCard.J), Card(FaceCard.A)),
        )
        self.assertEqual(
            collection.values,
            [765 * 1, 220 * 2, 28 * 3, 684 * 4, 483 * 5]
        )

    def test_value_calculation_when_jokers_wild(self):
        with jokers_wild():
            collection = HandCollection(
                Hand(765, Card(3), Card(2), Card(FaceCard.T), Card(3), Card(FaceCard.K)),
                Hand(684, Card(FaceCard.T), Card(5), Card(5), Card(FaceCard.J), Card(5)),
                Hand(28, Card(FaceCard.K), Card(FaceCard.K), Card(6), Card(7), Card(7)),
                Hand(220, Card(FaceCard.K), Card(FaceCard.T), Card(FaceCard.J), Card(FaceCard.J), Card(FaceCard.T)),
                Hand(483, Card(FaceCard.Q), Card(FaceCard.Q), Card(FaceCard.Q), Card(FaceCard.J), Card(FaceCard.A)),
            )
            self.assertEqual(
                collection.values,
                [765 * 1, 28 * 2, 684 * 3, 483 * 4, 220 * 5]
            )


class ParserTestCase(TestCase):
    def test_parser(self):
        input_data = StringIO("""32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483""")
        collection = get_hand_collection_from_input(input_data)
        self.assertEqual(
            collection.values,
            [765 * 1, 220 * 2, 28 * 3, 684 * 4, 483 * 5]
        )
