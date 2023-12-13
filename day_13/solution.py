def read(path: str) -> list[str]:
    with open(path, 'r', encoding='utf-8') as f:
        data = f.readlines()
    return [l.strip('\n') for l in data]


def split_examples(data: list[str]) -> list[list[str]]:
    """
    Split input data (list of str) into list of examples (each example is a list of str).
    """
    c = []
    examples = []
    for r in data:
        if r == '':
            examples.append(c)
            c = []
        else:
            c.append(r)
    if c:
        examples.append(c)
    return examples


def find_adjacent_duplicated_rows(data: list[str]) -> list[tuple[int, int]]:
    """
    Find in data identical rows which are adjacent to each other.
    """
    found = []
    for i in range(1, len(data)):
        if data[i - 1] == data[i]:
            found.append((i - 1, i))
    return found


def is_reflection(data: list[str], indices: tuple[int, int]) -> bool:
    """
    Check if there is reflection in data between rows with passed indices.
    """
    if indices[0] + 1 != indices[1]:
        raise ValueError('Incorrect duplicated rows indices')

    part1 = data[:indices[0] + 1]
    part2 = data[indices[1]:]

    pattern_len = min(len(part1), len(part2))

    return list(reversed(part1))[:pattern_len] == part2[:pattern_len]


def find_split_indices(data: list[str]) -> tuple[int, int] | None:
    """
    Find first row split indices in data (line of reflection is between those rows).
    """
    duplicated_rows = find_adjacent_duplicated_rows(data)

    for indices in duplicated_rows:
        if is_reflection(data, indices):
            return indices
    return None


def transpose[T: (list[list], list[str])](data: T) -> T:
    """
    Transpose matrix.
    """
    transposed = []

    for col_idx in range(len(data[0])):
        transposed_row = []
        for row in data:
            transposed_row.append(row[col_idx])
        if isinstance(data[0], str):
            transposed_row = ''.join(transposed_row)
        transposed.append(transposed_row)

    return transposed


def pattern_value(data: list[str], row_multiplier: int, col_multiplier: int) -> int:
    """
    Calculate pattern value for the example.
    """

    # row
    split_indices = find_split_indices(data)
    if split_indices:
        # We have to add 1, because rows/columns ale indexed from 1 in the example
        return row_multiplier * (split_indices[0] + 1)

    # columns
    data = transpose(data)
    split_indices = find_split_indices(data)
    if split_indices:
        return col_multiplier * (split_indices[0] + 1)

    raise ValueError('Incorrect pattern')


def differences_count(data: list[str], indices: tuple[int, int]) -> int:
    """
    Return number of differences in data mirrored between rows with passed indices.
    """
    if indices[0] + 1 != indices[1]:
        raise ValueError('Incorrect duplicated rows indices')

    part1 = data[:indices[0] + 1]
    part2 = data[indices[1]:]

    pattern_len = min(len(part1), len(part2))

    cnt = 0
    for row1, row2 in zip(list(reversed(part1))[:pattern_len], part2[:pattern_len]):
        for val1, val2 in zip(row1, row2):
            if val1 != val2:
                cnt += 1
    return cnt


def all_possible_splits(data_len: int, border_offset: int = 0) -> list[tuple[int, int]]:
    """
    Return all possible split indices (possible lines of reflection) for data with given len.
    """
    splits = []
    for i in range(0 + border_offset, data_len - border_offset):
        splits.append((i, i + 1))
    return splits


def find_split_indices_smudge(data: list[str]) -> tuple[int, int] | None:
    """
    Find first row split indices in data (line of reflection is between those rows).
    """
    splits = all_possible_splits(len(data))

    for indices in splits:
        if differences_count(data, indices) == 1:
            return indices
    return None


def pattern_value_when_1_smudge(data: list[str], row_multiplier: int, col_multiplier: int) -> int:
    """
    Calculate pattern value for the example when mirror has exactly one smudge.
    """

    # rows
    split_indices = find_split_indices_smudge(data)
    if split_indices:
        # We have to add 1, because rows/columns are indexed from 1 in the example
        return row_multiplier * (split_indices[0] + 1)

    # columns
    data = transpose(data)
    split_indices = find_split_indices_smudge(data)
    if split_indices:
        return col_multiplier * (split_indices[0] + 1)

    raise ValueError('Incorrect pattern')


if __name__ == '__main__':
    path = 'input.txt'

    data = read(path)
    examples = split_examples(data)
    row_multiplier = 100
    col_multiplier = 1

    # Part 1
    print(sum(pattern_value(e, row_multiplier, col_multiplier) for e in examples))

    # Part 2
    print(sum(pattern_value_when_1_smudge(e, row_multiplier, col_multiplier) for e in examples))
