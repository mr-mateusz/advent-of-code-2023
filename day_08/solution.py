import itertools


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


def count_steps(from_node: str, to_node: str, instructions: str, nodes: dict[str, dict[str, str]]) -> int:
    if from_node == to_node:
        return 0

    current_node = from_node
    instructions = itertools.cycle(instructions)

    for step_index, next_step in enumerate(instructions, 1):
        possible_ways = nodes[current_node]
        current_node = possible_ways[next_step]
        if current_node == to_node:
            return step_index


if __name__ == '__main__':
    path = 'input.txt'

    data = read(path)
    instructions = data[0]
    nodes = parse_nodes(data[2:])

    # Part 1
    steps = count_steps('AAA', 'ZZZ', instructions, nodes)
    print(steps)
