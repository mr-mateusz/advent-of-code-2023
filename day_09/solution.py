def read(path: str) -> list[str]:
    with open(path, 'r', encoding='utf-8') as f:
        data = f.readlines()
    return [l.strip('\n') for l in data]


def predict(observations: list[int]) -> int:
    obs_matrix = [observations[:]]

    while set(obs_matrix[-1]) != {0}:
        line = [next_ - prev for prev, next_ in zip(obs_matrix[-1][:-1], obs_matrix[-1][1:])]
        obs_matrix.append(line)

    obs_matrix[-1].append(0)
    prev_line_last_val = 0
    for line in reversed(obs_matrix[:-1]):
        last_val = line[-1]
        new_last_val = last_val + prev_line_last_val
        line.append(new_last_val)
        prev_line_last_val = new_last_val

    return obs_matrix[0][-1]


if __name__ == '__main__':
    path = 'input.txt'

    data = read(path)
    data = [[int(val) for val in line.split()] for line in data]

    # Part 1
    print(sum(predict(line) for line in data))
