import functools
import operator


def read(path: str) -> list[str]:
    with open(path, 'r', encoding='utf-8') as f:
        data = f.readlines()
    return [l.strip('\n') for l in data]


def parse(data: list[str]) -> list[dict]:
    times = data[0].split()
    distances = data[1].split()
    return [{'time': int(t), 'best_distance': int(d)} for t, d in zip(times[1:], distances[1:])]


def calc_distance(wait_time: int, total_time: int) -> int:
    """
    >>> calc_distance(3, 7)
    12
    >>> calc_distance(1, 3)
    2
    """
    if wait_time > total_time:
        raise ValueError()
    return (total_time - wait_time) * wait_time


def num_winning_strategies(race: dict) -> int:
    best_wait_time = race['time'] // 2

    strategy_time = best_wait_time
    winning_strategies = 0
    worse_strategy = False
    while not worse_strategy:
        dist = calc_distance(strategy_time, race['time'])
        if dist > race['best_distance']:
            winning_strategies += 1
            # todo - optimisation - divide/multiply by 2 in every step in order to find threshold
            strategy_time -= 1
        else:
            worse_strategy = True

    if not winning_strategies:
        return 0
    # Multiply by 2 in order to add strategies from the opposite sides (longer wait time instead of shorter)
    winning_strategies *= 2
    # If total race time is even whe have to subtract one
    if race['time'] % 2 == 0:
        winning_strategies -= 1

    return winning_strategies


# Part 2

def parse_one_race(data: list[str]) -> dict:
    time = int(''.join(data[0].split(':')[1].split()))
    distance = int(''.join(data[1].split(':')[1].split()))

    return {'time': time, 'best_distance': distance}


if __name__ == '__main__':
    path = 'input.txt'

    data = read(path)
    races = parse(data)

    # Part 1
    res = functools.reduce(operator.mul, (num_winning_strategies(race) for race in races))
    print(res)

    # Part 2
    race = parse_one_race(data)
    print(num_winning_strategies(race))
