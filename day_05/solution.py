import copy
from dataclasses import dataclass
from functools import cached_property
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

    @cached_property
    def source_end(self) -> int:
        return self.source_start + self.len_ - 1

    @cached_property
    def destination_end(self) -> int:
        return self.destination_start + self.len_ - 1

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

        ranges = list(sorted(ranges, key=lambda x: x.source_start))

        return cls(fl[0], fl[2], ranges)

    def __getitem__(self, key: int) -> int:
        for range_ in self.ranges:
            try:
                return range_[key]
            except KeyError:
                pass
        return key

    def map_ranges(self, ranges_to_map: list[list[int, int]]) -> list[list[int, int]]:
        ranges_to_map = copy.deepcopy(ranges_to_map)

        mapped = []

        for rtm in ranges_to_map:
            for mapping_range in self.ranges:
                #                   [mapping range]
                # [range to map]
                if rtm[1] < mapping_range.source_start:
                    mapped.append(rtm[:])
                    rtm = None
                    break
                #          [mapping range]
                # [range to map ...
                if rtm[0] < mapping_range.source_start:
                    mapped.append([rtm[0], mapping_range.source_start - 1])
                    rtm[0] = mapping_range.source_start
                # [   mapping range     ]
                # [ ...[range to map]
                if rtm[1] <= mapping_range.source_end:
                    mapped.append([mapping_range[rtm[0]], mapping_range[rtm[1]]])
                    rtm = None
                    break
                # [ mapping range]
                # [ ...[range to map]
                if rtm[0] <= mapping_range.source_end:
                    mapped.append([mapping_range[rtm[0]], mapping_range[mapping_range.source_end]])
                    rtm[0] = mapping_range.source_end + 1

            # [last mapping range]
            #                      [range to map]
            if rtm:
                mapped.append(rtm[:])

        return mapped


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

    def map_ranges(self, ranges: list[list[int, int]]) -> list[list[int, int]]:
        for map_ in self.maps:
            ranges = sorted(ranges, key=lambda x: x[0])
            ranges = merge_ranges(ranges)
            ranges = map_.map_ranges(ranges)

        ranges = sorted(ranges, key=lambda x: x[0])
        ranges = merge_ranges(ranges)
        return ranges


def merge_ranges(ranges: list[list[int, int]]) -> list[list[int, int]]:
    """
    >>> merge_ranges([[10, 20], [21, 30]])
    [[10, 30]]
    >>> merge_ranges([[10, 19], [21, 30]])
    [[10, 19], [21, 30]]
    >>> merge_ranges([[10, 19], [21, 30], [31, 40], [41, 41], [42, 43], [45, 50]])
    [[10, 19], [21, 43], [45, 50]]
    """
    if not ranges:
        return ranges

    merged = [ranges[0][:]]

    for range_ in ranges[1:]:
        if merged[-1][1] + 1 == range_[0]:
            merged[-1][1] = range_[1]
        else:
            merged.append(range_[:])

    return merged


if __name__ == '__main__':
    path = 'input.txt'

    data = read(path)

    # Part 1
    seed_numbers = extract_seed_numbers(data[0])
    almanac = Almanac.from_raw(data[2:])
    print(min(almanac[sn] for sn in seed_numbers))

    # Part 2
    seed_ranges = [seed_numbers[i: i + 2] for i in range(0, len(seed_numbers), 2)]

    seed_ranges = [[r[0], r[0] + r[1] - 1] for r in seed_ranges]

    result_ranges = almanac.map_ranges(seed_ranges)

    print(result_ranges[0][0])
