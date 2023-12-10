from enum import Enum
from typing import Self, NamedTuple

Position = tuple[int, int]

class Direction(Enum):
    NORTH = (-1, 0)
    SOUTH = (1, 0)
    WEST = (0, -1)
    EAST = (0, 1)

    @property
    def opposite(self) -> Self:
        return _opposite_directions[self]


_opposite_directions = {
    Direction.NORTH: Direction.SOUTH,
    Direction.SOUTH: Direction.NORTH,
    Direction.EAST: Direction.WEST,
    Direction.WEST: Direction.EAST
}

pipe_connections = {
    '|': {Direction.NORTH, Direction.SOUTH},
    '-': {Direction.WEST, Direction.EAST},
    'L': {Direction.NORTH, Direction.EAST},
    'J': {Direction.NORTH, Direction.WEST},
    '7': {Direction.SOUTH, Direction.WEST},
    'F': {Direction.SOUTH, Direction.EAST}
}


def read(path: str) -> list[str]:
    with open(path, 'r', encoding='utf-8') as f:
        data = f.readlines()
    return [l.strip() for l in data]


def find_start(data: list[list[str]], start_char: str = 'S') -> Position:
    for row_idx, row in enumerate(data):
        for col_idx, val in enumerate(row):
            if val == start_char:
                return row_idx, col_idx


def step(position: Position, direction: Direction) -> Position:
    """
    Take a step in a given direction
    """
    return tuple(p + d for p, d in zip(position, direction.value))


def find_connected(data: list[list[str]], position: Position) -> list[tuple[Position, Direction]]:
    found = []

    for direction in Direction:
        pos = step(position, direction)
        pipe = data[pos[0]][pos[1]]
        if direction.opposite in pipe_connections.get(pipe, set()):
            found.append((pos, direction.opposite))

    # [(position, coming_from)]
    return found


def next_position(data: list[list[str]],
                  position: tuple[tuple[int, int], Direction]) -> tuple[tuple[int, int], Direction]:
    position, coming_from = position

    pipe = data[position[0]][position[1]]
    another_direction = list(pipe_connections[pipe] - {coming_from})[0]

    return step(position, another_direction), another_direction.opposite


def find_farthest_point_dist(data: list[list[str]]) -> int:
    starting_pos = find_start(data)

    position_distances = {}

    steps = 1

    # position, direction_from
    position_1, position_2 = find_connected(data, starting_pos)

    position_distances[position_1[0]] = steps
    position_distances[position_2[0]] = steps

    while True:
        next_position_1 = next_position(data, position_1)
        next_position_2 = next_position(data, position_2)

        if next_position_1[0] in position_distances and next_position_2[0] in position_distances:
            return max(position_distances.values())

        steps += 1

        position_distances[next_position_1[0]] = steps
        position_distances[next_position_2[0]] = steps

        position_1 = next_position_1
        position_2 = next_position_2


if __name__ == '__main__':
    path = 'input.txt'

    data = read(path)

    data = [list(l) for l in data]

    print(find_farthest_point_dist(data))
