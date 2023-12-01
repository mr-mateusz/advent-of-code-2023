def read_lines(path: str) -> list[str]:
    with open(path, 'r', encoding='utf-8') as f:
        data = f.readlines()
    return [l.strip('\n') for l in data]


def recover_numbers_from_lines(data: list[str]) -> list[int]:
    numbers = []
    for line in data:
        digits = [l for l in line if l.isdigit()]
        numbers.append(int(digits[0] + digits[-1]))
    return numbers


_words = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']


def word_to_number(word: str, words: list[str] | None = None) -> int:
    words = words or _words
    return words.index(word)


def find_digits(line: str):
    digits = []
    for start_idx in range(len(line)):
        subword = line[start_idx:]
        if subword[0].isdigit():
            digits.append(int(subword[0]))
            continue
        for word in _words:
            if subword.startswith(word):
                digits.append(word_to_number(word))
                break
    return digits


def part_2(data: list[str], words: list[str]) -> list[int]:
    numbers = []
    for line in data:
        digits = find_digits(line)
        numbers.append(int(str(digits[0]) + str(digits[-1])))
    return numbers


if __name__ == "__main__":
    path = 'input.txt'

    data = read_lines(path)

    # part 1
    calibration_numbers = recover_numbers_from_lines(data)
    print(sum(calibration_numbers))

    # part 2
    calibration_numbers = part_2(data, _words)
    print(sum(calibration_numbers))
