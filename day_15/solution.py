from functools import cache


def read(path: str) -> list[str]:
    with open(path, 'r', encoding='utf-8') as f:
        data = f.readlines()
    return [l.strip('\n') for l in data]


calls_num = 0


@cache
def _hash(char: str, current_val: int = 0) -> int:
    global calls_num
    calls_num += 1
    print(f'Not found in cache {char=}, {current_val=}')
    current_val += ord(char)
    current_val *= 17
    current_val %= 256
    return current_val


def get_hash(text: str) -> int:
    res = 0
    for char in text:
        res = _hash(char, res)
    return res


if __name__ == '__main__':
    path = 'input.txt'

    data = read(path)[0]

    # Part 1
    print(sum(get_hash(step) for step in data.split(',')))

    print('cn', calls_num)
