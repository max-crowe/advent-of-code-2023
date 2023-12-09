#!/usr/bin/env python

import sys
from argparse import ArgumentParser
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from day2.calculator import Calculator
from day2.parser import get_games_from_input


parser = ArgumentParser()
parser.add_argument(
    "data",
    type=open,
)
parser.add_argument(
    "-r", "--red",
    type=int,
)
parser.add_argument(
    "-g", "--green",
    type=int,
)
parser.add_argument(
    "-b", "--blue",
    type=int,
)
parser.add_argument(
    "-m", "--mode",
    choices=["possibility", "viability"]
)


if __name__ == "__main__":
    args = parser.parse_args()
    result = 0
    calculator = Calculator(red=args.red, green=args.green, blue=args.blue)
    for game in get_games_from_input(args.data):
        if args.mode == "possibility":
            if calculator.get_game_possibility(game):
                result += game.id
        else:
            minimum_viable_set = game.get_minimum_viable_set()
            result += minimum_viable_set.red * minimum_viable_set.green * minimum_viable_set.blue
    print(result)
