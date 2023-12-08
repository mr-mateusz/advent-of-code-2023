import itertools
from typing import Callable


def read(path: str) -> list[str]:
    with open(path, 'r', encoding='utf-8') as f:
        data = f.readlines()
    return [l.strip('\n') for l in data]


def parse_nodes(lines: list[str]) -> dict[str, dict[str, str]]:
    nodes = {}
    for line in lines:
        node, lr = line.split('=')
        node = node.strip()

        l, r = lr.split(',')
        l = l.strip(' (')
        r = r.strip(' )')

        nodes[node] = {'L': l, 'R': r}
    return nodes


def count_steps(from_node: str, end_node: str | Callable[[str], bool], instructions: str,
                nodes: dict[str, dict[str, str]]) -> int:
    if isinstance(end_node, str):
        is_end_node = lambda x: x == end_node
    else:
        is_end_node = end_node

    if is_end_node(from_node):
        return 0

    current_node = from_node
    instructions = itertools.cycle(instructions)

    for step_index, next_step in enumerate(instructions, 1):
        possible_ways = nodes[current_node]
        current_node = possible_ways[next_step]
        if is_end_node(current_node):
            return step_index


def count_steps_many_nodes(initial_nodes: list[str], is_ending_node: Callable[[str], bool],
                           instructions: str, nodes: dict[str, dict[str, str]]) -> int:
    # Does not work (too slow)
    if all(is_ending_node(n) for n in initial_nodes):
        return 0

    current_nodes = initial_nodes
    instructions = itertools.cycle(instructions)

    for step_index, next_step in enumerate(instructions, 1):
        st = len([n for n in current_nodes if is_ending_node(n)])
        st = '*' if st else ''

        print(f'{step_index}, {current_nodes}, {next_step}, {st}')

        next_nodes = []
        for cn in current_nodes:
            possible_ways = nodes[cn]
            next_nodes.append(possible_ways[next_step])

        current_nodes = next_nodes

        if all(is_ending_node(n) for n in current_nodes):
            print(current_nodes)
            return step_index


def simulate(initial_nodes: list[str], is_ending_node: Callable[[str], bool], steps: int,
             instructions: str, nodes: dict[str, dict[str, str]]) -> dict[str, list[dict]]:
    current_nodes = initial_nodes
    instructions = itertools.cycle(instructions)

    ending_nodes_positions = {node: [] for node in initial_nodes}
    for step_index, next_step in enumerate(instructions, 1):
        next_nodes = []
        for cn in current_nodes:
            possible_ways = nodes[cn]
            next_nodes.append(possible_ways[next_step])

        current_nodes = next_nodes

        for initial_node, node in zip(initial_nodes, current_nodes):
            if is_ending_node(node):
                ending_nodes_positions[initial_node].append({'ending_node': node, 'steps': step_index})

        if steps == step_index:
            return ending_nodes_positions


def gcd(a: int, b: int) -> int:
    """
    >>> gcd(8, 12)
    4
    >>> gcd(12, 8)
    4
    >>> gcd(30, 35)
    5
    """
    if a < b:
        return gcd(b, a)
    if b == 0:
        return a
    return gcd(b, a % b)


def lcm(numbers: list[int]) -> int:
    """
    >>> lcm([8, 12])
    24
    >>> lcm([12, 8])
    24
    >>> lcm([8, 4])
    8
    """
    if len(numbers) < 2:
        raise ValueError
    if len(numbers) == 2:
        return int(numbers[0] * numbers[1] / gcd(*numbers))
    return lcm([numbers[0], lcm(numbers[1:])])


if __name__ == '__main__':
    path = 'input.txt'

    data = read(path)
    instructions = data[0]
    nodes = parse_nodes(data[2:])

    # Part 1
    steps = count_steps('AAA', 'ZZZ', instructions, nodes)
    print(steps)

    # Part 2
    initial_nodes = [n for n in nodes.keys() if n.endswith('A')]

    res = simulate(initial_nodes, lambda x: x.endswith('Z'), 100000, instructions, nodes)
    # Assumptions for LCM  (for each initial node)
    for initial_node, ending_steps in res.items():
        # Always ends in the same ending node
        assert len(set(e['ending_node'] for e in ending_steps)) == 1

        first_ending_step = ending_steps[0]['steps']
        # Instructions cycle ends in the ending node
        assert first_ending_step % len(instructions) == 0

        # Fixed number of steps between ending nodes (cycles between endings, no initial offset)
        for index, e in enumerate(ending_steps, 1):
            assert e['steps'] / first_ending_step == index

    steps_to_first_ending = [r[0]['steps'] for r in res.values()]
    print(lcm(steps_to_first_ending))
