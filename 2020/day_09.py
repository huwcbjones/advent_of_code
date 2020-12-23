from itertools import combinations
from typing import Iterable, List
from unittest import TestCase


def parse_input(data: Iterable[str]) -> List[int]:
    return [int(i.strip()) for i in data if i.strip()]


def find_invalid(data: List[int], preamble: int) -> int:
    for i in range(preamble, len(data) + 1):
        if not any(sum(p) == data[i] for p in combinations(data[i - preamble : i], 2)):
            return data[i]


def find_sum_set(data: List[int], target: int) -> List[int]:
    data_len = len(data)
    for i in range(data_len):
        if data[i] > target:
            continue
        for w in range(1, data_len - i):
            data_slice = data[i : i + w]
            if sum(data_slice) == target:
                return data_slice


def find_encryption_weakness(data: List[int], target: int) -> int:
    sum_set = find_sum_set(data, target)
    return min(sum_set) + max(sum_set)


class Day09Test(TestCase):
    def test_find_invalid(self):
        data = [35, 20, 15, 25, 47, 40, 62, 55, 65, 95, 102, 117, 150, 182, 127, 219]
        self.assertEqual(127, find_invalid(data, 5))
        self.assertEqual(
            100, find_invalid(list(range(1, 25 + 1)) + [26, 49, 100, 50], 25),
        )

    def test_find_sum_set(self):
        data = [35, 20, 15, 25, 47, 40, 62, 55, 65, 95, 102, 117, 150, 182, 127, 219]
        self.assertListEqual([15, 25, 47, 40], find_sum_set(data, 127))

    def test_find_encryption_weakness(self):
        data = [35, 20, 15, 25, 47, 40, 62, 55, 65, 95, 102, 117, 150, 182, 127, 219]
        self.assertEqual(62, find_encryption_weakness(data, 127))


if __name__ == "__main__":
    with open("day_09-input.txt", "r") as fh:
        data = parse_input(fh)

        part_1 = find_invalid(data, 25)
        print(part_1)  # Part 1: 25918798

        part_2 = find_encryption_weakness(data, part_1)
        print(part_2)  # Part 2: 3340942
