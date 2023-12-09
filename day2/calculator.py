from .game import Game, CubeSet


class Calculator:
    def __init__(self, red: int, green: int, blue: int):
        self.red = red
        self.green = green
        self.blue = blue

    def get_round_possibility(self, round: CubeSet) -> bool:
        return round.red <= self.red and round.green <= self.green and round.blue <= self.blue

    def get_game_possibility(self, game: Game) -> bool:
        return all(self.get_round_possibility(round) for round in game.rounds)
