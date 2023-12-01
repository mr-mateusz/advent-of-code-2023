def read_lines(path: str) -> list[str]:
    with open(path, 'r', encoding='utf-8') as f:
        data = f.readlines()
    return [l.strip('\n') for l in data]


def __digits_to_number(digits: list[int | str]) -> int:
    return int(str(digits[0]) + str(digits[-1]))


def digits_to_numbers(lines: list[list[int | str]]) -> list[int]:
    return [__digits_to_number(line) for line in lines]


def __find_digits_in_line(line: str) -> list[int]:
    return [int(c) for c in line if c.isdigit()]


def find_digits(data: list[str]) -> list[list[int]]:
    return [__find_digits_in_line(line) for line in data]


_words = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']


def word_to_number(word: str, words: list[str] | None = None) -> int:
    words = words or _words
    return words.index(word)


def __find_digits_and_digit_words_in_line(line: str) -> list[int]:
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


def find_digits_and_digit_words(data: list[str]) -> list[list[int]]:
    return [__find_digits_and_digit_words_in_line(line) for line in data]


if __name__ == "__main__":
    path = 'input.txt'

    data = read_lines(path)

    # part 1
    data_digits = find_digits(data)
    calibration_numbers = digits_to_numbers(data_digits)
    print(sum(calibration_numbers))

    # part 2
    data_digits = find_digits_and_digit_words(data)
    calibration_numbers = digits_to_numbers(data_digits)
    print(sum(calibration_numbers))
