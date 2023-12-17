from enum import Enum
from typing import NamedTuple, Self

import numpy as np
from tqdm import tqdm


def read(path: str) -> list[str]:
    with open(path, 'r', encoding='utf-8') as f:
        data = f.readlines()
    return [l.strip('\n') for l in data]


class Direction(Enum):
    NORTH = (-1, 0)
    SOUTH = (1, 0)
    WEST = (0, -1)
    EAST = (0, 1)

    @property
    def opposite(self) -> Self:
        return _opposite_directions[self]


_opposite_directions = {
    Direction.NORTH: Direction.SOUTH,
    Direction.SOUTH: Direction.NORTH,
    Direction.EAST: Direction.WEST,
    Direction.WEST: Direction.EAST
}


class Node(NamedTuple):
    position: tuple[int, int]
    steps_taken: int
    direction: Direction

    def move(self, direction: Direction) -> Self:
        new_pos = tuple(a + b for a, b in zip(self.position, direction.value))
        if self.direction == direction:
            return type(self)(new_pos, self.steps_taken + 1, direction)
        return type(self)(new_pos, 1, direction)


class NodeWithDistance(NamedTuple):
    node: Node
    distance: int


def is_out(node: Node, map_: np.array) -> bool:
    h, w = map_.shape
    is_inside = (0 <= node.position[0] < h and 0 <= node.position[1] < w)
    return not is_inside


def get_adjacent_nodes(map_: np.ndarray, node: Node,
                       direction_min_steps: int, direction_max_steps: int) -> list[NodeWithDistance]:
    if node.steps_taken < direction_min_steps and node.position != (0, 0):
        next_nodes = [node.move(node.direction)]
    else:
        next_nodes = [node.move(d) for d in Direction]

    # print('Before filter:')
    # for nn in next_nodes:
    #     print(nn)

    tmp = []
    for nn in next_nodes:
        # Node leaves the map
        if is_out(nn, map_):
            # print('*out', nn)
            continue
        # Opposite direction
        if nn.direction == node.direction.opposite:
            # print('*dir', nn)
            continue
        # Too many steps
        if nn.steps_taken > direction_max_steps:
            # print('*ste', nn)
            continue

        dist = map_[*nn.position]
        nnd = NodeWithDistance(nn, dist)
        tmp.append(nnd)

    next_nodes = tmp

    # print('After filter:')
    # for nn in next_nodes:
    #     print(nn)

    return next_nodes


def find_distance(map_: np.ndarray, initial_node: Node, ending_node_pos: tuple[int, int],
                  direction_min_steps: int, direction_max_steps: int) -> int:
    nodes_dists = {initial_node: 0}
    next_node_candidate = initial_node
    visited_nodes = set()
    to_visit_candidates = {}

    pbar = tqdm()
    while next_node_candidate:
        pbar.update(1)
        next_nodes = get_adjacent_nodes(map_, next_node_candidate, direction_min_steps, direction_max_steps)
        current_node_distance = nodes_dists[next_node_candidate]

        for n in next_nodes:
            distance_to_node = current_node_distance + n.distance
            try:
                old_distance = nodes_dists[n.node]
                new_distance = min(old_distance, distance_to_node)
                nodes_dists[n.node] = min(nodes_dists[n.node], distance_to_node)
                #
                if n.node not in visited_nodes:
                    to_visit_candidates[old_distance].remove(n.node)
                    if len(to_visit_candidates[old_distance]) == 0:
                        del to_visit_candidates[old_distance]
                    try:
                        to_visit_candidates[new_distance].add(n.node)
                    except KeyError:
                        to_visit_candidates[new_distance] = {n.node}
                #
            except KeyError:
                nodes_dists[n.node] = distance_to_node

                #
                try:
                    to_visit_candidates[distance_to_node].add(n.node)
                except KeyError:
                    to_visit_candidates[distance_to_node] = {n.node}
                #

        visited_nodes.add(next_node_candidate)

        try:
            _new_candidate = None
            while not _new_candidate:
                min_dist = min(to_visit_candidates.keys())
                _new_candidate = to_visit_candidates[min_dist].pop()
                if len(to_visit_candidates[min_dist]) == 0:
                    del to_visit_candidates[min_dist]
            next_node_candidate = _new_candidate
        except ValueError:
            next_node_candidate = None

    pbar.close()

    # print('Results:')
    # for k, v in nodes_dists.items():
    #     if k.position == ending_node_pos:
    #         print(k, v)

    return min(v for k, v in nodes_dists.items() if k.position == ending_node_pos
               and k.steps_taken >= direction_min_steps)


if __name__ == '__main__':
    path = 'input.txt'

    data = read(path)
    data = np.array([[int(v) for v in row] for row in data])

    initial_node = Node((0, 0), 0, Direction.EAST)
    ending_node_pos = tuple(a - 1 for a in data.shape)

    # Part 1
    r = find_distance(data, initial_node, ending_node_pos, 1, 3)
    print(r)

    # Part 2
    r = find_distance(data, initial_node, ending_node_pos, 4, 10)
    print(r)
