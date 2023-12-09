from io import StringIO
from unittest import TestCase

from .calculator import Calculator
from .game import Game, CubeSet
from .parser import get_games_from_input


class CalculatorTestCase(TestCase):
    def test_get_round_possibility(self):
        calculator = Calculator(red=12, green=13, blue=14)
        rounds = [
            CubeSet(blue=3, red=4),
            CubeSet(red=1, green=2, blue=6),
            CubeSet(green=2),
            CubeSet(blue=1, green=2),
            CubeSet(green=3, blue=4, red=1),
            CubeSet(green=1, blue=1),
            CubeSet(green=8, blue=6, red=20),
            CubeSet(blue=5, red=4, green=13),
            CubeSet(green=5, red=1),
            CubeSet(green=1, red=3, blue=6),
            CubeSet(green=3, red=6),
            CubeSet(green=3, blue=15, red=14),
            CubeSet(red=6, blue=1, green=3),
            CubeSet(blue=2, red=1, green=2),
        ]
        expected = [
            True,
            True,
            True,
            True,
            True,
            True,
            False,
            True,
            True,
            True,
            True,
            False,
            True,
            True
        ]
        self.assertEqual(
            [calculator.get_round_possibility(round) for round in rounds],
            expected,
        )

    def test_get_game_possibility(self):
        calculator = Calculator(red=12, green=13, blue=14)
        games = [
            Game(
                id=1,
                rounds=[
                    CubeSet(blue=3, red=4),
                    CubeSet(red=1, green=2, blue=6),
                    CubeSet(green=2),
                ]
            ),
            Game(
                id=2,
                rounds=[
                    CubeSet(blue=1, green=2),
                    CubeSet(green=3, blue=4, red=1),
                    CubeSet(green=1, blue=1),
                ]
            ),
            Game(
                id=3,
                rounds=[
                    CubeSet(green=8, blue=6, red=20),
                    CubeSet(blue=5, red=4, green=13),
                    CubeSet(green=5, red=1),
                ]
            ),
            Game(
                id=4,
                rounds=[
                    CubeSet(green=1, red=3, blue=6),
                    CubeSet(green=3, red=6),
                    CubeSet(green=3, blue=15, red=14),
                ]
            ),
            Game(
                id=5,
                rounds=[
                    CubeSet(red=6, blue=1, green=3),
                    CubeSet(blue=2, red=1, green=2),
                ]
            )
        ]
        expected = [True, True, False, False, True]
        self.assertEqual(
            [calculator.get_game_possibility(game) for game in games],
            expected,
        )


class ParserTestCase(TestCase):
    def test_get_games_from_input(self):
        input_data = StringIO("""Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green""")
        self.assertEqual(
            list(get_games_from_input(input_data)),
            [
                Game(
                    id=1,
                    rounds=[
                        CubeSet(blue=3, red=4),
                        CubeSet(red=1, green=2, blue=6),
                        CubeSet(green=2),
                    ]
                ),
                Game(
                    id=2,
                    rounds=[
                        CubeSet(blue=1, green=2),
                        CubeSet(green=3, blue=4, red=1),
                        CubeSet(green=1, blue=1),
                    ]
                ),
                Game(
                    id=3,
                    rounds=[
                        CubeSet(green=8, blue=6, red=20),
                        CubeSet(blue=5, red=4, green=13),
                        CubeSet(green=5, red=1),
                    ]
                ),
                Game(
                    id=4,
                    rounds=[
                        CubeSet(green=1, red=3, blue=6),
                        CubeSet(green=3, red=6),
                        CubeSet(green=3, blue=15, red=14),
                    ]
                ),
                Game(
                    id=5,
                    rounds=[
                        CubeSet(red=6, blue=1, green=3),
                        CubeSet(blue=2, red=1, green=2),
                    ]
                )
            ]
        )


class GameTestCase(TestCase):
    def test_get_minimum_viable_set(self):
        games = [
            Game(
                id=1,
                rounds=[
                    CubeSet(blue=3, red=4),
                    CubeSet(red=1, green=2, blue=6),
                    CubeSet(green=2),
                ]
            ),
            Game(
                id=2,
                rounds=[
                    CubeSet(blue=1, green=2),
                    CubeSet(green=3, blue=4, red=1),
                    CubeSet(green=1, blue=1),
                ]
            ),
            Game(
                id=3,
                rounds=[
                    CubeSet(green=8, blue=6, red=20),
                    CubeSet(blue=5, red=4, green=13),
                    CubeSet(green=5, red=1),
                ]
            ),
            Game(
                id=4,
                rounds=[
                    CubeSet(green=1, red=3, blue=6),
                    CubeSet(green=3, red=6),
                    CubeSet(green=3, blue=15, red=14),
                ]
            ),
            Game(
                id=5,
                rounds=[
                    CubeSet(red=6, blue=1, green=3),
                    CubeSet(blue=2, red=1, green=2),
                ]
            )
        ]
        expected = [
            CubeSet(red=4, green=2, blue=6),
            CubeSet(red=1, green=3, blue=4),
            CubeSet(red=20, green=13, blue=6),
            CubeSet(red=14, green=3, blue=15),
            CubeSet(red=6, green=3, blue=2),
        ]
        self.assertEqual(
            [game.get_minimum_viable_set() for game in games],
            expected,
        )
