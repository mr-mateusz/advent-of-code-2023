from enum import Enum
from typing import Self, NamedTuple


class Position(NamedTuple):
    x: int
    y: int


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


class PositionVisit(NamedTuple):
    position: Position
    coming_from: Direction


def read(path: str) -> list[str]:
    with open(path, 'r', encoding='utf-8') as f:
        data = f.readlines()
    return [l.strip() for l in data]


def find_start(data: list[list[str]], start_char: str = 'S') -> Position:
    """
    Find starting position.
    """
    for row_idx, row in enumerate(data):
        for col_idx, val in enumerate(row):
            if val == start_char:
                return Position(row_idx, col_idx)


def step(position: Position, direction: Direction) -> Position:
    """
    Take a step in a given direction.
    """
    return Position(*[p + d for p, d in zip(position, direction.value)])


def find_connected(data: list[list[str]], position: Position) -> list[PositionVisit]:
    """
    Find position of pipes connected to the given position.
    """
    found = []
    for direction in Direction:
        pos = step(position, direction)
        pipe = data[pos[0]][pos[1]]
        # It means the pipe is connected in the direction we came from
        # Opposite -> we went NORTH, so it means we came from SOUTH
        if direction.opposite in pipe_connections.get(pipe, set()):
            found.append(PositionVisit(pos, direction.opposite))
    return found


def next_position(data: list[list[str]], position: PositionVisit) -> PositionVisit:
    """
    Move to the next position.
    (we know where we came from, so we can find out next position based on the type of the pipe)
    """
    position, coming_from = position

    pipe = data[position[0]][position[1]]
    another_direction = list(pipe_connections[pipe] - {coming_from})[0]

    return PositionVisit(step(position, another_direction), another_direction.opposite)


def find_pipe_pos_with_dists(data: list[list[str]]) -> dict[Position, int]:
    starting_pos = find_start(data)
    position_distances = {}
    steps = 1

    position_distances[starting_pos] = 0

    # We are going both ways simultaneously
    position_1, position_2 = find_connected(data, starting_pos)

    # Replace S in data with actual Pipe ;)
    # (If needed, its position can be found in the positions_distances dict -> the only position with distance 0)
    starting_pipe_directions = {position_1.coming_from.opposite, position_2.coming_from.opposite}
    for pipe_shape, directions in pipe_connections.items():
        if directions == starting_pipe_directions:
            data[starting_pos[0]][starting_pos[1]] = pipe_shape

    # Log number of steps it takes to reach given positions
    position_distances[position_1.position] = steps
    position_distances[position_2.position] = steps

    while True:
        # Go one step further in each way
        next_position_1 = next_position(data, position_1)
        next_position_2 = next_position(data, position_2)

        # Check if the whole pipe loop was already traversed
        if next_position_1.position in position_distances and next_position_2.position in position_distances:
            return position_distances

        steps += 1

        position_distances[next_position_1.position] = steps
        position_distances[next_position_2.position] = steps

        position_1 = next_position_1
        position_2 = next_position_2


def process_line(line: list[str], row_index: int, pipe_positions: set[Position]) -> int:
    """
    Each occurrence of SOUTH direction 'opens' or 'closes' intervals which means 'inside' or 'outside' pipe loop.
    """
    found_inside = 0
    is_inside = False
    for col_idx, pipe in enumerate(line):
        position = Position(row_index, col_idx)
        if position in pipe_positions:
            if Direction.SOUTH in pipe_connections[pipe]:
                is_inside = not is_inside
        else:
            if is_inside:
                found_inside += 1
    return found_inside


def find_area(data: list[list[str]], pipe_positions: set[Position]) -> int:
    total = 0
    for line_index, line in enumerate(data):
        total += process_line(line, line_index, pipe_positions)
    return total


if __name__ == '__main__':
    path = 'input.txt'

    data = read(path)
    data = [list(l) for l in data]

    # Part 1
    pipe_dists = find_pipe_pos_with_dists(data)
    print(max(pipe_dists.values()))

    # Part 2
    pipe_positions = set(pipe_dists.keys())
    print(find_area(data, pipe_positions))
