from collections import Counter, defaultdict
from math import prod
from typing import Dict, Iterable, List
from unittest import TestCase


def parse_adapters(data: Iterable[str]) -> List[int]:
    return [int(i) for i in data if i.strip()]


def test_adapters(adapters: List[int]) -> Dict[int, int]:
    adapters_to_check = sorted(adapters) + [max(adapters) + 3]
    joltage_differences = defaultdict(int)
    joltage = 0

    for adapter in adapters_to_check:
        joltage_difference = adapter - joltage
        if joltage_difference <= 3:
            joltage_differences[joltage_difference] += 1
            joltage = adapter
    return joltage_differences


def get_arrangement_count(adapters: List[int]) -> int:
    counter = Counter({0: 1})
    adapters = [0] + sorted(adapters)
    for adapter in adapters:
        counter[adapter + 1] += counter[adapter]
        counter[adapter + 2] += counter[adapter]
        counter[adapter + 3] += counter[adapter]
    return counter[max(adapters) + 3]


class Day10Test(TestCase):
    def test_test_adapters(self):
        self.assertDictEqual(
            {1: 7, 3: 5}, test_adapters([16, 10, 15, 5, 1, 11, 7, 19, 6, 12, 4])
        )
        self.assertDictEqual(
            {1: 22, 3: 10},
            test_adapters(
                [28, 33, 18, 42, 31, 14, 46, 20, 48, 47, 24, 23, 49, 45, 19]
                + [38, 39, 11, 1, 32, 25, 35, 8, 17, 7, 9, 4, 2, 34, 10, 3]
            ),
        )

    def test_get_all_arrangements(self):
        self.assertEqual(3, get_arrangement_count([1, 2, 4]))
        self.assertEqual(
            8, get_arrangement_count([16, 10, 15, 5, 1, 11, 7, 19, 6, 12, 4]),
        )
        self.assertEqual(
            19208,
            get_arrangement_count(
                [28, 33, 18, 42, 31, 14, 46, 20, 48, 47, 24, 23, 49, 45, 19]
                + [38, 39, 11, 1, 32, 25, 35, 8, 17, 7, 9, 4, 2, 34, 10, 3]
            ),
        )


if __name__ == "__main__":
    with open("day_10-input.txt", "r") as fh:
        adapters = parse_adapters(fh)

        part_1 = prod(test_adapters(adapters).values())
        print(part_1)  # Part 1: 2475

        part_2 = get_arrangement_count(adapters)
        print(part_2)  # Part 2: 442136281481216
