from dataclasses import dataclass
from enum import Enum
from typing import NamedTuple, Self


def read(path: str) -> list[str]:
    with open(path, 'r', encoding='utf-8') as f:
        data = f.readlines()
    return [l.strip('\n') for l in data]


class Direction(Enum):
    NORTH = (-1, 0)
    SOUTH = (1, 0)
    WEST = (0, -1)
    EAST = (0, 1)


class Position(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Position(*[a + b for a, b in zip(self, other)])


@dataclass
class Platform:
    width: int
    height: int
    round_rocks: set[Position]
    cube_rocks: set[Position]

    @classmethod
    def from_map(cls, map_: list[str]) -> Self:
        width = len(map_[0])
        height = len(map_)
        round_rocks = []
        cube_rocks = []

        for x, row in enumerate(map_):
            for y, val in enumerate(row):
                if val == 'O':
                    round_rocks.append(Position(x, y))
                elif val == '#':
                    cube_rocks.append(Position(x, y))

        return cls(width, height, set(round_rocks), set(cube_rocks))

    def can_move(self, rock: Position, direction: Direction) -> bool:
        new_pos = rock + direction.value
        if new_pos.x < 0:
            return False
        if new_pos.y < 0:
            return False
        if new_pos.x >= self.height:
            return False
        if new_pos.y >= self.width:
            return False
        if new_pos in self.round_rocks:
            return False
        if new_pos in self.cube_rocks:
            return False
        return True

    def move_north(self) -> None:
        rocks = sorted(self.round_rocks, key=lambda x: x.x)

        for rock in rocks:
            old_pos = rock
            new_pos = rock
            while self.can_move(new_pos, Direction.NORTH):
                new_pos += Direction.NORTH.value
            if new_pos != old_pos:
                self.round_rocks.remove(old_pos)
                self.round_rocks.add(new_pos)

    def __str__(self) -> str:
        data = [['.' for _ in range(self.width)] for _ in range(self.height)]
        for row_idx in range(self.height):
            for col_idx in range(self.width):
                if (row_idx, col_idx) in self.round_rocks:
                    data[row_idx][col_idx] = 'O'
                elif (row_idx, col_idx) in self.cube_rocks:
                    data[row_idx][col_idx] = '#'

        return '\n'.join(''.join(row) for row in data)

    def total_value(self) -> int:
        total = 0
        for rock in self.round_rocks:
            total += get_value(rock, self.height)
        return total


def get_value(rock: Position, height: int) -> int:
    return height - rock.x


if __name__ == '__main__':
    path = 'input.txt'

    data = read(path)

    platform = Platform.from_map(data)

    # Part 1
    platform.move_north()
    print(platform.total_value())
