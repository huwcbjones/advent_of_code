from itertools import permutations
from math import prod
from typing import Iterable, Tuple, List, Optional
from unittest import TestCase


def convert_entries(input: Iterable[str]) -> List[int]:
    return sorted([int(i) for i in input])


def find_entries(entries: Iterable[int], target: int = 2020, count: int = 2) -> Optional[Tuple[int, ...]]:
    for values in permutations(entries, count):
        if sum(values) == target:
            return values
    return None


def calculate_expenses(input: Iterable[str], count: int) -> int:
    entries = convert_entries(input)
    values = find_entries(entries, count=count)
    assert values is not None
    return prod(values)


class FindEntriesTest(TestCase):
    input = [
        "1721",
        "979",
        "366",
        "299",
        "675",
        "1456",
    ]

    def setUp(self) -> None:
        self.entries = convert_entries(self.input)

    def test_convert_entries(self):
        self.assertListEqual([299, 366, 675, 979, 1456, 1721], self.entries)

    def test_part_1(self):
        self.assertTupleEqual((299, 1721), find_entries(self.entries, count=2))
        self.assertEqual(514579, calculate_expenses(self.input, 2))

    def test_part_2(self):
        self.assertTupleEqual((366, 675, 979), find_entries(self.entries, count=3))
        self.assertEqual(241861950, calculate_expenses(self.input, 3))


if __name__ == "__main__":
    with open("day_01-input.txt", "r") as fh:
        print(calculate_expenses(fh, 2))
        fh.seek(0)
        print(calculate_expenses(fh, 3))
