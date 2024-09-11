from functools import cache


# recursive approach with splitting into two parts (split on first dot)

# _ 1,1,3
# 1  1,3
# 1,1 3
# 1,1,3 _

# 1,1,3 3
# [], [], [1,1,3]
# [], [1], [1,3]
# [], [1,1], [3]
# [], [1,1,3], []
# [1], [], [1,3]
# [1], [1], [3]
# [1], [1, 3], []
# [1,1], [], [3]
# [1,1], [3], []
# [1,1,3], [], []


def fill(record_part: str, char: str) -> str:
    return record_part.replace('?', char, 1)


def is_ok(record_part: str, values: list[int]) -> bool:
    return [len(n) for n in record_part.split('.') if n] == list(values)


def is_partial_ok(record_part: str, values: list[int]) -> bool:
    filled_values = [r for r in record_part.split('.') if r]
    ff = []
    last_one = None
    for f in filled_values:
        if '?' in f:
            last_one = f
            break
        ff.append(len(f))

    if ff != values[:len(ff)]:
        return False

    if not last_one:
        return True

    try:
        to_check = values[len(ff)]
    except IndexError:
        return last_one.count('#') == 0

    return True


def calculate_possible_assignments_in_part(record_part: str, values: list[int]) -> int:
    values = list(values)

    if values == []:
        if '#' in record_part:
            return 0
        else:
            return 1

    if sum(values) + len(values) - 1 > len(record_part):
        # print('guard')
        return 0

    if '?' not in record_part:
        if is_ok(record_part, values):
            return 1
        else:
            return 0

    if is_partial_ok(record_part, values):
        lp = calculate_possible_assignments_in_part(fill(record_part, '#'), values)
        rp = calculate_possible_assignments_in_part(fill(record_part, '.'), values)
        return lp + rp
    return 0


@cache
def doit(record: str, values: tuple[int]) -> int:
    values = list(values)

    if values == []:
        if '#' not in record:
            return 1
        return 0

    if '?' not in record:
        if is_ok(record, values):
            return 1
        return 0

    if sum(values) + len(values) - 1 > len(record):
        return 0

    record = record.strip('.')

    if not is_partial_ok(record, values):
        return 0

    if '.' not in record:
        return doit(fill(record, '#'), tuple(values)) + doit(fill(record, '.'), tuple(values))
    # split
    left, right = record.split('.', 1)
    total = 0
    for i in range(len(values) + 1):

        l = doit(left, tuple(values[:i]))
        if l == 0:
            total += 0
        else:
            r = doit(right, tuple(values[i:]))
            total += l * r
    return total


def main():
    input_file = 'input.txt'

    with open(input_file, 'r') as f:
        lines = f.readlines()

    # Part 1
    total = 0
    for line in lines[:]:
        record, values_str = line.split()
        values = [int(i) for i in values_str.split(',')]
        possible_arrangements = doit(record, tuple(values))
        total += possible_arrangements

    print(total)

    # Part 2
    total = 0
    for line in lines[:]:
        record, values_str = line.split()
        values = [int(i) for i in values_str.split(',')]
        record += '?'
        record *= 5
        record = record[:-1]
        values *= 5
        possible_arrangements = doit(record, tuple(values))
        total += possible_arrangements

    print(total)


if __name__ == "__main__":
    main()
