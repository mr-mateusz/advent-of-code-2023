from __future__ import annotations

from typing import Callable


def read(path: str) -> list[str]:
    with open(path, 'r', encoding='utf-8') as f:
        data = f.readlines()
    return [l.strip('\n') for l in data]


def parse(row: str) -> tuple[str, list[int]]:
    record, expected_groups = row.split()
    expected_groups = [int(v) for v in expected_groups.split(',')]
    return record, expected_groups


def create_tree(depth: int) -> Node:
    root = Node()

    last_layer = [root]
    for _ in range(depth):
        new_last_layer = []
        for node in last_layer:
            nodes = [Node('.'), Node('#')]
            node.kids = nodes
            new_last_layer.extend(nodes)
        last_layer = new_last_layer
    return root


class Node:
    def __init__(self, value: str | None = None, kids: list[Node] | None = None) -> None:
        self.value = value
        self.kids = kids or []

    def process(self, already_set: list[str], test_func: Callable) -> int:
        if not self.value:
            # print(self.value, self.kids, already_set + [self.value])
            return sum(k.process(already_set, test_func) for k in self.kids)

        already_set = already_set + [self.value]
        if not test_func(already_set):
            # print(self.value, self.kids, already_set, test_func(already_set), 0)
            return 0

        if not self.kids:
            # print(self.value, self.kids, already_set, test_func(already_set), 1)
            return 1

        # print(self.value, self.kids, already_set, test_func(already_set))
        return sum(k.process(already_set, test_func) for k in self.kids)


def fill(record: str, values: list[str]) -> str:
    filled = []
    values_iter = iter(values)
    for char in record:
        if char == '?':
            try:
                filled.append(next(values_iter))
            except StopIteration:
                filled.append(char)
        else:
            filled.append(char)
    return ''.join(filled)


def count_groups(record: str) -> list[int]:
    groups = []
    current_group = 0
    for char in record:
        if char == '.' and current_group:
            groups.append(current_group)
            current_group = 0
        if char == '#':
            current_group += 1
        if char == '?':
            if current_group:
                groups.append(current_group)
            groups.append(0)  # Temporary solution
            return groups

    if current_group:
        groups.append(current_group)
    return groups


def can_create(partial_groups: list[int], expected_groups: list[int]) -> bool:
    if not partial_groups:
        return False
    if partial_groups == [0]:
        return True

    if partial_groups[-1] == 0:
        last_le = True
        partial_groups = partial_groups[:-1]
    else:
        last_le = False

    if len(expected_groups) < len(partial_groups):
        return False

    if last_le:
        to_compare = partial_groups[:-1]
    else:
        to_compare = partial_groups

    if last_le:
        for a, b in zip(to_compare, expected_groups):
            if a != b:
                return False
        if partial_groups[-1] > expected_groups[len(partial_groups) - 1]:
            return False
    else:
        return partial_groups == expected_groups
    return True


def possible_sequences_cnt(row: str) -> int:
    record, expected_groups = parse(row)

    # print(record)
    # print(expected_groups)

    to_fill = record.count('?')

    # print(to_fill)

    tree = create_tree(to_fill)

    # print(tree)

    def test_func(values: list[str]) -> bool:
        filled_record = fill(record, values)

        partial_groups = count_groups(filled_record)

        return can_create(partial_groups, expected_groups)

    return tree.process([], test_func)


if __name__ == '__main__':
    path = 'input.txt'

    data = read(path)

    # Part 1
    print(sum(possible_sequences_cnt(row) for row in data))
