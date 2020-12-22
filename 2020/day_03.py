from collections import deque
from enum import Enum
from math import prod
from typing import List, Deque, TypeVar, Iterable, Union, Tuple, Sequence
from unittest import TestCase


class Square(str, Enum):
    TREE = "#"
    OPEN = "."

    @classmethod
    def values(cls):
        """Values of this enum"""
        if not hasattr(cls, "__values__"):
            setattr(cls, "__values__", set(i.value for i in cls))
        return getattr(cls, "__values__")

    @classmethod
    def contains(cls, value):
        """Returns whether the Enum contains the given value"""
        return value in cls.values()


T = TypeVar("T")


class RingBuffer(deque, Deque[T]):
    def __getitem__(self, index) -> T:
        if isinstance(index, int):
            index %= len(self)
        return super().__getitem__(index)


Map = List[RingBuffer[Square]]


def parse_map(input: Iterable[str]) -> Map:
    return [
        RingBuffer([Square(c) for c in l if Square.contains(c)], maxlen=len(l))
        for l in input
    ]


def count_trees(map: Map, right: int, down: int) -> int:
    x, y = (right, down)
    tree_count = 0
    while y < len(map):
        if map[y][x] == Square.TREE:
            tree_count += 1
        x += right
        y += down
    return tree_count


SLOPES = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]


def check_slopes(map: Map, slopes: Sequence[Tuple[int, int]] = None) -> List[int]:
    slopes = slopes or SLOPES
    results = []
    for x, y in slopes:
        results.append(count_trees(map, x, y))
    return results


class Day03Test(TestCase):
    input = (
        "..##.......",
        "#...#...#..",
        ".#....#..#.",
        "..#.#...#.#",
        ".#...##..#.",
        "..#.##.....",
        ".#.#.#....#",
        ".#........#",
        "#.##...#...",
        "#...##....#",
        ".#..#...#.#",
    )

    def setUp(self) -> None:
        self.map = parse_map(self.input)

    def test_parse_map(self):
        self.assertListEqual(
            [
                RingBuffer(
                    [
                        Square.OPEN,
                        Square.OPEN,
                        Square.TREE,
                        Square.TREE,
                        Square.OPEN,
                        Square.OPEN,
                        Square.OPEN,
                        Square.OPEN,
                        Square.OPEN,
                        Square.OPEN,
                        Square.OPEN,
                    ],
                    maxlen=11,
                ),
                RingBuffer(
                    [
                        Square.TREE,
                        Square.OPEN,
                        Square.OPEN,
                        Square.OPEN,
                        Square.TREE,
                        Square.OPEN,
                        Square.OPEN,
                        Square.OPEN,
                        Square.TREE,
                        Square.OPEN,
                        Square.OPEN,
                    ],
                    maxlen=11,
                ),
            ],
            self.map[0:2],
        )

    def test_count_trees(self):
        self.assertEqual(7, count_trees(self.map, 3, 1))

    def test_check_slopes(self):
        self.assertListEqual([2, 7, 3, 4, 2], check_slopes(self.map))


if __name__ == "__main__":
    with open("day_03-input.txt", "r") as fh:
        map = parse_map(fh)
        print(count_trees(map, 3, 1))
        print(prod(check_slopes(map)))
