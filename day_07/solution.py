from collections import Counter
from dataclasses import dataclass
from functools import cached_property
from typing import Self


def read(path: str) -> list[str]:
    with open(path, 'r', encoding='utf-8') as f:
        data = f.readlines()
    return [l.strip('\n') for l in data]


__rank2val = {
    'A': 14,
    'K': 13,
    'Q': 12,
    'J': 11,
    'T': 10,
}


def rank2val(rank: str) -> int:
    try:
        return __rank2val[rank]
    except KeyError:
        return int(rank)


@dataclass
class Hand:
    cards: str
    bid: int

    @classmethod
    def from_str(cls, str_: str) -> Self:
        cards, bid = str_.split()
        return cls(cards, int(bid))

    @cached_property
    def type(self) -> tuple:
        return tuple(count for _, count in Counter(self.cards).most_common())

    @cached_property
    def values(self) -> tuple:
        return tuple(rank2val(c) for c in self.cards)

    def __lt__(self, other: Self) -> bool:
        if not isinstance(other, type(self)):
            raise NotImplemented
        if self.type == other.type:
            return self.values < other.values
        return self.type < other.type

    def __eq__(self, other: Self) -> bool:
        if not isinstance(other, type(self)):
            raise NotImplemented
        return self.type == other.type and self.values == other.values


if __name__ == '__main__':
    path = 'input.txt'

    data = read(path)
    hands = [Hand.from_str(line) for line in data]

    # Part 1
    print(sum(index * hand.bid for index, hand in enumerate(sorted(hands), 1)))
