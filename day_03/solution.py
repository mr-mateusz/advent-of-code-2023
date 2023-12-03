from collections.abc import Iterable
from typing import NamedTuple, Self


def read(path: str) -> list[str]:
    with open(path, 'r', encoding='utf-8') as f:
        data = f.readlines()
    data = [line.strip('\n') for line in data]
    return data


def read_gen(path: str) -> Iterable[str]:
    is_eof = False
    with open(path, 'r', encoding='utf-8') as f:
        while not is_eof:
            data = f.readline()
            if data == '':
                is_eof = True
            else:
                data = data.strip('\n')
                yield data


def scan_line(line: str) -> tuple[list[tuple[tuple[int], int]], set[int]]:
    """Scan the passed line and return indices of the found symbols as well as found numbers and their indices.

    >>> scan_line('617*......')
    ([((0, 1, 2), 617)], {3})
    """
    symbol_indices = []
    numbers = []

    current_number_indices = []
    current_number_digits = []
    for index, char in enumerate(line):
        if char.isdigit():
            current_number_indices.append(index)
            current_number_digits.append(char)
        else:
            if current_number_indices:
                numbers.append((tuple(current_number_indices), int(''.join(current_number_digits))))
                current_number_indices = []
                current_number_digits = []
            if char != '.':  # it means it must be a symbol at this moment
                symbol_indices.append(index)

    if current_number_indices:
        numbers.append((tuple(current_number_indices), int(''.join(current_number_digits))))

    symbol_indices = set(symbol_indices)
    return numbers, symbol_indices


def find_part_numbers_in_line(prev_line_symbol_indices: set[int],
                              curr_line_symbol_indices: set[int], curr_line_numbers: list[tuple[tuple[int], int]],
                              next_line_symbol_indices: set[int]) -> list[int]:
    found_part_numbers = []
    for number_indices, number in curr_line_numbers:
        neighbours = [number_indices[0] - 1, number_indices[-1] + 1]
        number_indices_extended = list(number_indices) + neighbours
        # Check if symbol is adjacent in the previous line
        if any(index in prev_line_symbol_indices for index in number_indices_extended):
            found_part_numbers.append(number)

        # Check if symbol is adjacent in the current line
        if any(index in curr_line_symbol_indices for index in neighbours):
            found_part_numbers.append(number)

        # Check if symbol is adjacent in the next line
        if any(index in next_line_symbol_indices for index in number_indices_extended):
            found_part_numbers.append(number)

    return found_part_numbers


def find_part_numbers_sum(lines_iter: Iterable[str]) -> int:
    lines_iter = iter(lines_iter)

    # Initialize variables for the first line
    prev_line_symbol_indices = set()
    curr_line_numbers, curr_line_symbol_indices = [], set()
    next_line_numbers, next_line_symbol_indices = scan_line(next(lines_iter))

    total_sum = 0
    for line in lines_iter:
        prev_line_symbol_indices = curr_line_symbol_indices
        curr_line_numbers, curr_line_symbol_indices = next_line_numbers, next_line_symbol_indices
        next_line_numbers, next_line_symbol_indices = scan_line(line)

        line_numbers = find_part_numbers_in_line(prev_line_symbol_indices,
                                                 curr_line_symbol_indices, curr_line_numbers,
                                                 next_line_symbol_indices)

        total_sum += sum(line_numbers)

    # Run for the last line
    prev_line_symbol_indices = curr_line_symbol_indices
    curr_line_symbol_indices, curr_line_numbers = next_line_symbol_indices, next_line_numbers
    next_line_symbol_indices, next_line_numbers = set(), []

    line_numbers = find_part_numbers_in_line(prev_line_symbol_indices,
                                             curr_line_symbol_indices, curr_line_numbers,
                                             next_line_symbol_indices)

    total_sum += sum(line_numbers)

    return total_sum


# Ok, first part was overcomplicated (additional challenge was to iterate over every row only once),
# so now let's do it the easy way

def to_number(digits: list[str]) -> int:
    return int(''.join(digits))


class Position(NamedTuple):
    x: int
    y: int


class NumberPosition(NamedTuple):
    value: int
    positions: tuple[Position, ...]

    @classmethod
    def from_lists(cls, digits: list[str], positions: list[Position]) -> Self:
        return cls(to_number(digits), tuple(positions))


def maximum_distance(pos1: Position, pos2: Position) -> int:
    """
    https://en.wikipedia.org/wiki/Chebyshev_distance

    >>> maximum_distance(Position(1,1), Position(1,1))
    0
    >>> maximum_distance(Position(1,1), Position(1,2))
    1
    >>> maximum_distance(Position(1,1), Position(2,2))
    1
    >>> maximum_distance(Position(1,1), Position(2,3))
    2
    """
    return max(abs(pos1.x - pos2.x), abs(pos1.y - pos2.y))


def is_adjacent(num: NumberPosition, pos: Position) -> bool:
    """
    >>> is_adjacent(NumberPosition(467, (Position(0, 0), Position(0, 1), Position(0, 2))), Position(0,3))
    True
    >>> is_adjacent(NumberPosition(467, (Position(0, 0), Position(0, 1), Position(0, 2))), Position(0,4))
    False
    >>> is_adjacent(NumberPosition(467, (Position(0, 0), Position(0, 1), Position(0, 2))), Position(1,1))
    True
    >>> is_adjacent(NumberPosition(467, (Position(0, 0), Position(0, 1), Position(0, 2))), Position(1,3))
    True
    >>> is_adjacent(NumberPosition(467, (Position(0, 0), Position(0, 1), Position(0, 2))), Position(1,4))
    False
    """
    return min(maximum_distance(num_pos, pos) for num_pos in num.positions) == 1


def symbol_positions_iter(data: list[list], symbol: str = '*') -> Iterable[Position]:
    positions = []
    for row_idx, row in enumerate(data):
        for col_idx, char in enumerate(row):
            if char == symbol:
                yield Position(row_idx, col_idx)


def find_numbers(data: list[str]) -> list[NumberPosition]:
    positions = []
    for row_idx, row in enumerate(data):
        current_number_indices = []
        current_number_digits = []
        for col_idx, char in enumerate(row):
            if char.isdigit():
                current_number_indices.append(Position(row_idx, col_idx))
                current_number_digits.append(char)
            else:
                if current_number_indices:
                    positions.append(NumberPosition.from_lists(current_number_digits, current_number_indices))
                    current_number_indices = []
                    current_number_digits = []

        if current_number_indices:
            positions.append(NumberPosition.from_lists(current_number_digits, current_number_indices))

    return positions


def find_gear_ratios_sum(data: list[str]) -> int:
    numbers = find_numbers(data)

    gear_rations_sum = 0
    for symbol_position in symbol_positions_iter(data):
        found_adjacent_numbers = []
        for number in numbers:
            if is_adjacent(number, symbol_position):
                found_adjacent_numbers.append(number)

                if len(found_adjacent_numbers) == 2:
                    gear_rations_sum += found_adjacent_numbers[0].value * found_adjacent_numbers[1].value
                    break
    return gear_rations_sum


if __name__ == '__main__':
    path = 'input.txt'

    # Part 1
    gen = read_gen(path)
    print(find_part_numbers_sum(gen))

    # Part 2
    data = read(path)
    print(find_gear_ratios_sum(data))
