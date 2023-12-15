from dataclasses import dataclass
from enum import Enum
from functools import cache
from typing import Self


def read(path: str) -> list[str]:
    with open(path, 'r', encoding='utf-8') as f:
        data = f.readlines()
    return [l.strip('\n') for l in data]


# _hash_calls_num = 0
# get_hash_calls_num = 0


@cache
def _hash(char: str, current_val: int = 0) -> int:
    # global _hash_calls_num
    # _hash_calls_num += 1
    # print(f'Not found in cache {char=}, {current_val=}')
    current_val += ord(char)
    current_val *= 17
    current_val %= 256
    return current_val


@cache
def get_hash(text: str) -> int:
    # global get_hash_calls_num
    # get_hash_calls_num += 1
    # print(f'Not found in cache {text=}')
    res = 0
    for char in text:
        res = _hash(char, res)
    return res


class OperationType(Enum):
    REMOVE = '-'
    UPSERT = '='


@dataclass
class Operation:
    box_index: int
    label: str
    focal_length: int | None
    operation_type: OperationType

    @classmethod
    def from_str(cls, s: str) -> Self:
        if '=' in s:
            label, focal_length = s.split('=')
            focal_length = int(focal_length)
            operation_type = OperationType.UPSERT
        elif '-' in s:
            label = s[:-1]
            focal_length = None
            operation_type = OperationType.REMOVE
        else:
            raise ValueError('Incorrect operation str')
        box_index = get_hash(label)

        return cls(box_index, label, focal_length, operation_type)


def calc_focusing_power(box_index: int, slot: int, focal_length: int) -> int:
    """
    >>> calc_focusing_power(0, 1, 1)
    1
    >>> calc_focusing_power(3, 2, 5)
    40
    >>> calc_focusing_power(3, 3, 6)
    72
    """
    return (box_index + 1) * slot * focal_length


def perform_initialization(boxes: list[dict], initialisation_sequence: str) -> int:
    for op_str in initialisation_sequence.split(','):
        operation = Operation.from_str(op_str)

        if operation.operation_type == OperationType.REMOVE:
            box = boxes[operation.box_index]
            try:
                del box[operation.label]
            except KeyError:
                pass
        elif operation.operation_type == OperationType.UPSERT:
            boxes[operation.box_index][operation.label] = operation.focal_length
        else:
            raise ValueError('Incorrect Operation Type')

    total_fp = 0
    for box_index, box in enumerate(boxes):
        for slot_index, (lens_label, lens_value) in enumerate(box.items(), 1):
            total_fp += calc_focusing_power(box_index, slot_index, lens_value)

    return total_fp


if __name__ == '__main__':
    path = 'input.txt'

    data = read(path)[0]

    # Part 1
    print(sum(get_hash(step) for step in data.split(',')))

    # Part 2
    boxes_cnt = 256
    boxes = [dict() for _ in range(boxes_cnt)]
    total_focusing_power = perform_initialization(boxes, data)
    print(total_focusing_power)

    # print('_hcn', _hash_calls_num)
    # print('hgcn', get_hash_calls_num)

# Some experiments with cache
# full cache
# _hcn 2518
# hgcn 2686
#
#
# no cache
# _hcn 31645
# hgcn 8000
#
#
# # _hash cache only
# _hcn 2518
# hgcn 8000
#
#
# # get_hash cache only
# _hcn 12394
# hgcn 2686
