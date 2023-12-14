import itertools
import time
from collections.abc import Sequence
from dataclasses import dataclass
from enum import Enum
from typing import NamedTuple, Self

from tqdm import tqdm


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

    def _get_sorted_rocks_for_move(self, direction: Direction) -> list[Position]:
        if direction == Direction.NORTH:
            return sorted(self.round_rocks, key=lambda x: x.x)
        elif direction == Direction.SOUTH:
            return sorted(self.round_rocks, key=lambda x: x.x, reverse=True)
        elif direction == Direction.WEST:
            return sorted(self.round_rocks, key=lambda x: x.y)
        elif direction == Direction.EAST:
            return sorted(self.round_rocks, key=lambda x: x.y, reverse=True)
        raise ValueError()

    def move(self, direction: Direction) -> None:
        rocks = self._get_sorted_rocks_for_move(direction)

        for rock in rocks:
            old_pos = rock
            new_pos = rock
            while self.can_move(new_pos, direction):
                new_pos += direction.value
            if new_pos != old_pos:
                self.round_rocks.remove(old_pos)
                self.round_rocks.add(new_pos)

    def move_cycle(self):
        self.move(Direction.NORTH)
        self.move(Direction.WEST)
        self.move(Direction.SOUTH)
        self.move(Direction.EAST)

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


def timeit(func):
    def wrapped(*args, **kwargs):
        st = time.time()
        res = func(*args, **kwargs)
        en = time.time()
        print(f'Time taken: {en - st}')
        return res

    return wrapped


@timeit
def find_pattern(seq: Sequence) -> tuple[None, None] | tuple[int, int]:
    for offset in range(len(seq) // 2):
        max_pattern_len = (len(seq) - offset) // 2
        for pattern_len in range(1, max_pattern_len):
            chunk_iter = iter(seq[offset:])
            first_chunk = list(itertools.islice(chunk_iter, pattern_len))

            # Assume that there is a cycle with given len
            all_match = True

            while chunk := list(itertools.islice(chunk_iter, pattern_len)):
                if len(chunk) != len(first_chunk):
                    # last chunk
                    break
                if chunk != first_chunk:
                    # pattern does not match
                    all_match = False
                    break

            if all_match:
                return offset, pattern_len

    return None, None


def find_value(steps: int, offset_values: list[int], cycle_values: list[int]) -> int:
    if steps < len(offset_values):
        return offset_values[steps]
    remaining = steps - len(offset_values)
    value_in_cycle = remaining % len(cycle_values)
    return cycle_values[value_in_cycle]


if __name__ == '__main__':
    path = 'input.txt'

    data = read(path)

    # Part 1
    platform = Platform.from_map(data)
    platform.move(Direction.NORTH)
    print(platform.total_value())

    # Part 2

    # Simulation in order to find pattern
    platform = Platform.from_map(data)

    simulation_steps = 1000

    history = []
    history.append(platform.total_value())
    for _ in tqdm(range(simulation_steps), total=simulation_steps):
        platform.move_cycle()
        history.append(platform.total_value())

    offset, cycle_len = find_pattern(history)

    if offset and cycle_len:
        print(f'Pattern found. {offset=}, {cycle_len=}')

    pattern_offset_values = history[:offset]
    pattern_cycle_values = history[offset: offset + cycle_len]

    # Sanity check
    assert find_value(simulation_steps, pattern_offset_values, pattern_cycle_values) == history[-1]

    cycles_num = 1_000_000_000
    print(find_value(cycles_num, pattern_offset_values, pattern_cycle_values))
