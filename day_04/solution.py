from collections.abc import Iterable
from dataclasses import dataclass
from typing import Self


def read(path: str) -> list[str]:
    with open(path, 'r', encoding='utf-8') as f:
        data = f.readlines()
    data = [line.strip('\n') for line in data]
    return data


def __to_set(numbers_str: str) -> set[int]:
    """
    >>> __to_set('1 2 3')
    {1, 2, 3}
    >>> __to_set(' 3 4 5 ')
    {3, 4, 5}
    """
    numbers = numbers_str.strip().split()
    return set(int(num) for num in numbers)


def _parse_card_raw(line: str) -> tuple[int, set[int], set[int]]:
    card_info, numbers = line.split(':')

    _, card_id = card_info.split()
    card_id = int(card_id)

    winning_numbers, actual_numbers = numbers.split('|')

    winning_numbers = __to_set(winning_numbers)
    actual_numbers = __to_set(actual_numbers)

    return card_id, winning_numbers, actual_numbers


@dataclass
class Card:
    id_: int
    winning_numbers: set[int]
    actual_numbers: set[int]

    @classmethod
    def from_str(cls, card_str: str) -> Self:
        return cls(*_parse_card_raw(card_str))

    @property
    def value(self) -> int:
        overlapping_cnt = len(self.winning_numbers & self.actual_numbers)

        if overlapping_cnt == 0:
            return 0

        return 2 ** (overlapping_cnt - 1)


def total_value(data: Iterable[str]) -> int:
    return sum(Card.from_str(line).value for line in data)


if __name__ == '__main__':
    path = 'input.txt'

    # change to generator
    data = read(path)

    # Part 1
    print(total_value(data))
