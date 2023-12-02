from dataclasses import dataclass
from typing import Self


def read_data(path: str) -> list[str]:
    with open(path, 'r', encoding='utf-8') as f:
        data = f.readlines()
    data = [l.strip('\n') for l in data]
    return data


@dataclass
class CubesSet:
    red: int = 0
    green: int = 0
    blue: int = 0

    @classmethod
    def from_round_str(cls, round_: str) -> Self:
        cubes_str = round_.split(',')
        print(cubes_str)
        cubes_dct = {}
        for cube_str in cubes_str:
            cube_str = cube_str.strip()
            cnt, color = cube_str.split()
            cubes_dct[color] = int(cnt)
        print(cubes_dct)
        return cls(**cubes_dct)

def is_possible(other):
    pass


@dataclass
class Game:
    id_: int
    rounds: list[CubesSet]


    @classmethod
    def from_game_str(cls, game: str) -> Self:
        game_str, rounds_str = game.split(':')
        print(game_str)
        print(rounds_str)

        _, game_id = game_str.split()

        print(game_id)

        rounds_str = rounds_str.split(';')
        print(rounds_str)

        rounds = [CubesSet.from_round_str(round_str) for round_str in rounds_str]

        print(rounds)
        return cls(game_id, rounds)


if __name__ == '__main__':
    path = 'input2.txt'

    games_raw = read_data(path)

    game_str = games_raw[0]

    print(game_str)

    for game_str in games_raw:
        Game.from_game_str(game_str)
