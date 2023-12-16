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


def _move(ray: tuple[int, int, Direction]) -> tuple[int, int, Direction]:
    return ray[0] + ray[2].value[0], ray[1] + ray[2].value[1], ray[2]


def _move_mirror_back(ray: tuple[int, int, Direction]) -> tuple[int, int, Direction]:
    if ray[2] == Direction.EAST:
        return _move((ray[0], ray[1], Direction.SOUTH))
    elif ray[2] == Direction.NORTH:
        return _move((ray[0], ray[1], Direction.WEST))
    elif ray[2] == Direction.WEST:
        return _move((ray[0], ray[1], Direction.NORTH))
    elif ray[2] == Direction.SOUTH:
        return _move((ray[0], ray[1], Direction.EAST))
    raise ValueError()


def _move_mirror(ray: tuple[int, int, Direction]) -> tuple[int, int, Direction]:
    if ray[2] == Direction.EAST:
        return _move((ray[0], ray[1], Direction.NORTH))
    elif ray[2] == Direction.NORTH:
        return _move((ray[0], ray[1], Direction.EAST))
    elif ray[2] == Direction.WEST:
        return _move((ray[0], ray[1], Direction.SOUTH))
    elif ray[2] == Direction.SOUTH:
        return _move((ray[0], ray[1], Direction.WEST))
    raise ValueError()


def _move_horizontal_splitter(ray: tuple[int, int, Direction]) -> list[tuple[int, int, Direction]]:
    if ray[2] in (Direction.EAST, Direction.WEST):
        return [_move(ray)]
    elif ray[2] in (Direction.NORTH, Direction.SOUTH):
        return [_move((ray[0], ray[1], Direction.WEST)), _move((ray[0], ray[1], Direction.EAST))]
    raise ValueError()


def _move_vertical_splitter(ray: tuple[int, int, Direction]) -> list[tuple[int, int, Direction]]:
    if ray[2] in (Direction.NORTH, Direction.SOUTH):
        return [_move(ray)]
    elif ray[2] in (Direction.EAST, Direction.WEST):
        return [_move((ray[0], ray[1], Direction.NORTH)), _move((ray[0], ray[1], Direction.SOUTH))]
    raise ValueError()


def move(ray: tuple[int, int, Direction], tile: str) -> list[tuple[int, int, Direction]]:
    if tile == '.':
        return [_move(ray)]
    elif tile == '\\':
        return [_move_mirror_back(ray)]
    elif tile == '/':
        return [_move_mirror(ray)]
    elif tile == '-':
        return _move_horizontal_splitter(ray)
    elif tile == '|':
        return _move_vertical_splitter(ray)

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

    def energized_tiles(self) -> list[tuple[int, int]]:
        return list(set(t[:2] for t in self.visited_positions))

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
        for ray in self.rays:
            tile = self.get_tile(ray)
            rays_moved = move(ray, tile)
            # If the ray has left the contraption we don't track it anymore
            rays_moved = [rm for rm in rays_moved if self.is_inside(rm)]
            # This position is already visited by ray which came from the same direction
            # there is no need to track it anymore, because it will repeat path of the previous ray
            rays_moved = [rm for rm in rays_moved if rm not in self.visited_positions]

            rays_after_step.extend(rays_moved)

        self.visited_positions.update(rays_after_step)
        self.rays = rays_after_step

    def simulate(self) -> None:
        while self.rays:
            self.step()


if __name__ == '__main__':
    path = 'input.txt'

    data = read(path)

    # Part 1
    ray = (0, 0, Direction.EAST)
    contraption = Contraption.from_map(data)
    contraption.add_ray(ray)
    contraption.simulate()

    print(len(contraption.energized_tiles()))
