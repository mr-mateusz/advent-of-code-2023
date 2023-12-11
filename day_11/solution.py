def read(path: str) -> list[str]:
    with open(path, 'r', encoding='utf-8') as f:
        data = f.readlines()
    return [l.strip('\n') for l in data]


def find_rows_without_galaxies(data: list[str]) -> list[int]:
    found = []
    for index, row in enumerate(data):
        if set(row) == {'.'}:
            found.append(index)
    return found


def find_cols_without_galaxies(data: list[str]) -> list[int]:
    found = []
    for index in range(len(data[0])):
        if set(v[index] for v in data) == {'.'}:
            found.append(index)
    return found


def find_galaxies(data: list[str]) -> list[tuple[int, int]]:
    found = []
    for row_idx, row in enumerate(data):
        for col_idx, val in enumerate(row):
            if val == '#':
                found.append((row_idx, col_idx))
    return found


def manhattan_dist(pos1: tuple[int, int], pos2: tuple[int, int]) -> int:
    """
    >>> manhattan_dist((3, 4), (5, 7))
    5
    >>> manhattan_dist((5, 7), (3, 4))
    5
    """
    return sum(abs(a - b) for a, b in zip(pos1, pos2))


def count_numbers(numbers: list[int], range_: tuple[int, int]) -> int:
    lb, ub = min(range_), max(range_)
    i = 0
    for n in numbers:
        if lb < n < ub:
            i += 1
    return i


def galaxies_dist(galaxy1: tuple[int, int], galaxy2: tuple[int, int], expanded_rows: list[int],
                  expanded_cols: list[int]) -> int:
    dist = manhattan_dist(galaxy1, galaxy2)

    rows_correction = count_numbers(expanded_rows, (galaxy1[0], galaxy2[0]))
    cols_correction = count_numbers(expanded_cols, (galaxy1[1], galaxy2[1]))

    return dist + rows_correction + cols_correction


def galaxies_dists_sum(galaxies: tuple[int, int], expanded_rows: list[int], expanded_cols: list[int]) -> int:
    total = 0
    for index, g1 in enumerate(galaxies):
        for g2 in galaxies[index + 1:]:
            total += galaxies_dist(g1, g2, expanded_rows, expanded_cols)
    return total


if __name__ == '__main__':
    path = 'input.txt'

    data = read(path)

    rows_without_galaxies = find_rows_without_galaxies(data)
    cols_without_galaxies = find_cols_without_galaxies(data)
    galaxies = find_galaxies(data)

    # Part 1
    print(galaxies_dists_sum(galaxies, rows_without_galaxies, cols_without_galaxies))
