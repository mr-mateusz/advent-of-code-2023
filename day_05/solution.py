from dataclasses import dataclass
from typing import Self


def read(path: str) -> list[str]:
    with open(path, 'r', encoding='utf-8') as f:
        data = f.readlines()
    return [l.strip('\n') for l in data]


def extract_seed_numbers(line: str) -> list[int]:
    return [int(num) for num in line.split(':')[1].strip().split()]


@dataclass(frozen=True)
class MapRange:
    source_start: int
    destination_start: int
    len_: int

    @classmethod
    def from_str(cls, s: str) -> Self:
        d, s, l = [int(v) for v in s.split()]
        return cls(s, d, l)

    def __getitem__(self, key: int) -> int:
        if self.source_start <= key < self.source_start + self.len_:
            offset = key - self.source_start
            return self.destination_start + offset
        raise KeyError()


@dataclass(frozen=True)
class Map:
    # from_ and to added to handle cases when maps are not in order (todo)
    from_: str
    to: str
    ranges: list[MapRange]

    @classmethod
    def from_raw(cls, data: list[str]) -> Self:
        fl = data[0].split()[0].split('-')

        ranges = [MapRange.from_str(line) for line in data[1:]]

        return cls(fl[0], fl[2], ranges)

    def __getitem__(self, key: int) -> int:
        for range_ in self.ranges:
            try:
                return range_[key]
            except KeyError:
                pass
        return key


@dataclass(frozen=True)
class Almanac:
    maps: list[Map]

    @classmethod
    def from_raw(cls, data: list[str]) -> Self:
        maps = []
        lines = []
        for line in data:
            if not line:
                maps.append(Map.from_raw(lines))
                lines = []
            else:
                lines.append(line)

        if lines:
            maps.append(Map.from_raw(lines))

        return cls(maps)

    def __getitem__(self, key: int) -> int:
        """Map seed to location"""
        # Todo - handle case in which maps are not in order
        for map_ in self.maps:
            key = map_[key]
        return key


if __name__ == '__main__':
    path = 'input.txt'

    data = read(path)

    # Part 1
    seed_numbers = extract_seed_numbers(data[0])
    almanac = Almanac.from_raw(data[2:])
    print(min(almanac[sn] for sn in seed_numbers))
