from dataclasses import dataclass
from enum import Enum
from typing import Self


def read(path: str) -> list[str]:
    with open(path, 'r', encoding='utf-8') as f:
        data = f.readlines()
    return [l.strip('\n') for l in data]


class Direction(Enum):
    NORTH = (-1, 0)
    SOUTH = (1, 0)
    WEST = (0, -1)
    EAST = (0, 1)


def move(ray: tuple[int, int, Direction], tile: str) -> tuple[int, int, Direction]:
    if tile == '.':
        return ray[0] + ray[2].value[0], ray[1] + ray[2].value[1], ray[2]
    elif tile == '\\':
        # only for test -> implement correctly
        return ray[0] + ray[2].value[0], ray[1] + ray[2].value[1], ray[2]

    raise NotImplementedError()

@dataclass
class Contraption:
    width: int
    height: int

    special_tiles: dict[str, set[tuple[int, int]]]

    rays: list[tuple[int, int, Direction]]
    visited_positions: set[tuple[int, int, Direction]]

    @classmethod
    def from_map(cls, map_: list[str]) -> Self:
        width = len(map_[0])
        height = len(map_)

        special_tiles = {  # todo SpecialTile enum
            '\\': set(),
            '/': set(),
            '-': set(),
            '|': set()
        }

        for row_idx, row in enumerate(map_):
            for col_idx, val in enumerate(row):
                for special_tile, positions in special_tiles.items():
                    if val == special_tile:
                        positions.add((row_idx, col_idx))
                        break

        return cls(width, height, special_tiles, [], set())

    def add_ray(self, ray: tuple[int, int, Direction]) -> None:
        if ray not in self.visited_positions:
            self.rays.append(ray)
            self.visited_positions.add(ray)

    def is_inside(self, ray: tuple[int, int, Direction]) -> bool:
        if ray[0] < 0 or self.height <= ray[0]:
            return False
        if ray[1] < 0 or self.width <= ray[1]:
            return False
        return True

    def get_tile(self, position: tuple) -> str:
        for special_tile, positions in self.special_tiles.items():
            if position[:2] in positions:
                return special_tile
        return '.'

    def step(self) -> None:
        rays_after_step = []
        print(f'Rays to move: {len(self.rays)}')
        for ray in self.rays:
            tile = self.get_tile(ray)
            print(f'Moving: {ray}, which is on tile: {tile}')
            ray_moved = move(ray, tile)
            print(f'After move: {ray_moved}')
            # If the ray has left the contraption we don't track it anymore
            if not self.is_inside(ray_moved):
                print(f'*Left contraption: {ray_moved}')  # debug
                continue
            # This position is already visited by ray which came from the same direction
            # there is no need to track it anymore, because it will repeat path of the previous ray
            if ray_moved in self.visited_positions:
                print(f'*Position already visited: {ray_moved}')
                continue
            rays_after_step.append(ray_moved)

        self.visited_positions.update(rays_after_step)
        self.rays = rays_after_step


if __name__ == '__main__':
    path = 'input2.txt'

    data = read(path)

    print(data)

    data = ['.' * 5 for _ in range(5)]

    data[0] = '....\\'

    print(data)

    contraption = Contraption.from_map(data)
    contraption.add_ray((0, 0, Direction.EAST))
    contraption.add_ray((2, 2, Direction.NORTH))
    print(contraption)

    for _ in range(3):
        contraption.step()

    print(contraption)

    contraption.add_ray((4, 2, Direction.NORTH))

    print(contraption)

    for _ in range(2):
        contraption.step()

    print(contraption)
