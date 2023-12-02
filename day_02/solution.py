from __future__ import annotations

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
        cubes_dct = {}
        for cube_str in cubes_str:
            cube_str = cube_str.strip()
            cnt, color = cube_str.split()
            cubes_dct[color] = int(cnt)
        return cls(**cubes_dct)

    def is_possible(self, other: CubesSet) -> bool:
        return self.red <= other.red and self.green <= other.green and self.blue <= other.blue


@dataclass
class Game:
    id_: int
    rounds: list[CubesSet]


    @classmethod
    def from_game_str(cls, game: str) -> Self:
        game_str, rounds_str = game.split(':')

        _, game_id = game_str.split()
        game_id = int(game_id)

        rounds_str = rounds_str.split(';')

        rounds = [CubesSet.from_round_str(round_str) for round_str in rounds_str]

        return cls(game_id, rounds)

    def is_possible(self, cubes: CubesSet) -> bool:
        return all(round_.is_possible(cubes) for round_ in self.rounds)


if __name__ == '__main__':
    path = 'input.txt'

    games_raw = read_data(path)

    games = [Game.from_game_str(game_str) for game_str in games_raw]

    # Part 1
    cubes_total = CubesSet(12, 13, 14)

    possible_games = [game for game in games if game.is_possible(cubes_total)]
    print(sum(game.id_ for game in possible_games))

