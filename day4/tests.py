from io import StringIO
from unittest import TestCase

from .card import Card, set_winnings
from .parser import get_cards_from_input

class CardTestCase(TestCase):
    def test_get_value(self):
        self.assertEqual(
            Card(id=1, winning_numbers={41, 48, 83, 86, 17}, numbers={83, 86, 6, 31, 17, 9, 48, 53}).value,
            8
        )
        self.assertEqual(
            Card(id=2, winning_numbers={13, 32, 20, 16, 61}, numbers={61, 30, 68, 82, 17, 32, 24, 19}).value,
            2
        )
        self.assertEqual(
            Card(id=3, winning_numbers={1, 21, 53, 59, 44}, numbers={69, 82, 63, 72, 16, 21, 14, 1}).value,
            2
        )
        self.assertEqual(
            Card(id=4, winning_numbers={41, 92, 73, 84, 69}, numbers={59, 84, 76, 51, 58, 5, 54, 83}).value,
            1
        )
        self.assertEqual(
            Card(id=5, winning_numbers={87, 83, 26, 28, 32}, numbers={88, 30, 70, 12, 93, 22, 82, 36}).value,
            0
        )
        self.assertEqual(
            Card(id=6, winning_numbers={31, 18, 13, 56, 72}, numbers={74, 77, 10, 23, 35, 67, 36, 11}).value,
            0
        )

    def test_get_length(self):
        card = Card(
            id=1,
            won_cards=[
                Card(
                    id=2,
                    won_cards=[
                        Card(
                            id=3,
                            won_cards=[Card(id=4)]
                        ),
                        Card(id=5)
                    ]
                ),
                Card(
                    id=6,
                    won_cards=[
                        Card(id=7)
                    ]
                ),
                Card(id=8)
            ]
        )
        self.assertEqual(len(card), 8)

    def test_set_winnings(self):
        cards = [
            Card(id=1, winning_numbers={41, 48, 83, 86, 17}, numbers={83, 86, 6, 31, 17, 9, 48, 53}),
            Card(id=2, winning_numbers={13, 32, 20, 16, 61}, numbers={61, 30, 68, 82, 17, 32, 24, 19}),
            Card(id=3, winning_numbers={1, 21, 53, 59, 44}, numbers={69, 82, 63, 72, 16, 21, 14, 1}),
            Card(id=4, winning_numbers={41, 92, 73, 84, 69}, numbers={59, 84, 76, 51, 58, 5, 54, 83}),
            Card(id=5, winning_numbers={87, 83, 26, 28, 32}, numbers={88, 30, 70, 12, 93, 22, 82, 36}),
            Card(id=6, winning_numbers={31, 18, 13, 56, 72}, numbers={74, 77, 10, 23, 35, 67, 36, 11})
        ]
        set_winnings(cards)
        self.assertEqual(sum(len(card) for card in cards), 30)


class ParserTestCase(TestCase):
    def test_get_cards_from_input(self):
        input_data = StringIO("""Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11""")
        self.assertEqual(
            list(get_cards_from_input(input_data)),
            [
                Card(id=1, winning_numbers={41, 48, 83, 86, 17}, numbers={83, 86, 6, 31, 17, 9, 48, 53}),
                Card(id=2, winning_numbers={13, 32, 20, 16, 61}, numbers={61, 30, 68, 82, 17, 32, 24, 19}),
                Card(id=3, winning_numbers={1, 21, 53, 59, 44}, numbers={69, 82, 63, 72, 16, 21, 14, 1}),
                Card(id=4, winning_numbers={41, 92, 73, 84, 69}, numbers={59, 84, 76, 51, 58, 5, 54, 83}),
                Card(id=5, winning_numbers={87, 83, 26, 28, 32}, numbers={88, 30, 70, 12, 93, 22, 82, 36}),
                Card(id=6, winning_numbers={31, 18, 13, 56, 72}, numbers={74, 77, 10, 23, 35, 67, 36, 11})
            ]
        )
