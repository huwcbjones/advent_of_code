from __future__ import annotations

from copy import deepcopy
from enum import Enum
from itertools import product
from typing import Callable, List, Tuple
from unittest import TestCase


class Seat(str, Enum):
    FLOOR = "."
    EMPTY = "L"
    OCCUPIED = "#"

    def __repr__(self):
        return self.value


Seats = List[List[Seat]]


def count_adjacent_occupied_seats(layout: Seats, column: int, row: int) -> int:
    count = 0
    for y in range(max(row - 1, 0), min(row + 2, len(layout))):
        for x in range(max(column - 1, 0), min(column + 2, len(layout[row]))):
            if y == row and x == column:
                continue
            if layout[y][x] is Seat.OCCUPIED:
                count += 1
    return count


def count_visible_occupied_seats(layout: Seats, column: int, row: int) -> int:
    count = 0
    for vector in product([-1, 0, 1], repeat=2):
        if vector == (0, 0):
            continue
        x = column + vector[0]
        y = row + vector[1]
        while 0 <= y < len(layout) and 0 <= x < len(layout[row]):
            if layout[y][x] in (Seat.OCCUPIED, Seat.EMPTY):
                if layout[y][x] is Seat.OCCUPIED:
                    count += 1
                break
            x += vector[0]
            y += vector[1]
    return count


def simulate(
    layout: Seats,
    min_occupied_seats: int = 4,
    seat_count_func: Callable[[Seats, int, int], int] = count_adjacent_occupied_seats,
) -> Tuple[Seats, bool]:
    new_layout = deepcopy(layout)
    changes_made = False
    for y, row in enumerate(layout):
        for x, p in enumerate(row):
            if p is Seat.FLOOR:
                continue

            occupied_seat_count = seat_count_func(layout, x, y)

            if p is Seat.EMPTY and occupied_seat_count == 0:
                new_layout[y][x] = Seat.OCCUPIED
                changes_made = True

            if p is Seat.OCCUPIED and occupied_seat_count >= min_occupied_seats:
                new_layout[y][x] = Seat.EMPTY
                changes_made = True

    return new_layout, changes_made


def simulate_until_no_changes(
    layout: Seats,
    min_occupied_seats: int = 4,
    seat_count_func: Callable[[Seats, int, int], int] = count_adjacent_occupied_seats,
) -> Seats:
    changes_made = True
    iteration_count = 0
    while changes_made:
        layout, changes_made = simulate(layout, min_occupied_seats, seat_count_func)
        iteration_count += 1
    return layout


def count_occupied_seats(layout: Seats) -> int:
    return [j for i in layout for j in i].count(Seat.OCCUPIED)


def layout_from_string(layout: str) -> Seats:
    return [[Seat(c) for c in row] for row in layout.splitlines(False)]


def string_from_layout(seats: Seats) -> str:
    return "\n".join("".join(s.value for s in row) for row in seats)


class Day11Test(TestCase):
    INITIAL_LAYOUT = "\n".join(
        (
            "L.LL.LL.LL",
            "LLLLLLL.LL",
            "L.L.L..L..",
            "LLLL.LL.LL",
            "L.LL.LL.LL",
            "L.LLLLL.LL",
            "..L.L.....",
            "LLLLLLLLLL",
            "L.LLLLLL.L",
            "L.LLLLL.LL",
        )
    )

    def assertLayoutEqual(self, expected: str, actual: Seats):
        self.assertEqual(expected, string_from_layout(actual))

    def test_simulate_p1(self):
        layout = layout_from_string(self.INITIAL_LAYOUT)

        layout, _ = simulate(layout)
        with self.subTest("iteration 1"):
            self.assertLayoutEqual(
                "\n".join(
                    (
                        "#.##.##.##",
                        "#######.##",
                        "#.#.#..#..",
                        "####.##.##",
                        "#.##.##.##",
                        "#.#####.##",
                        "..#.#.....",
                        "##########",
                        "#.######.#",
                        "#.#####.##",
                    )
                ),
                layout,
            )

        layout, _ = simulate(layout)
        with self.subTest("iteration 2"):
            self.assertLayoutEqual(
                "\n".join(
                    (
                        "#.LL.L#.##",
                        "#LLLLLL.L#",
                        "L.L.L..L..",
                        "#LLL.LL.L#",
                        "#.LL.LL.LL",
                        "#.LLLL#.##",
                        "..L.L.....",
                        "#LLLLLLLL#",
                        "#.LLLLLL.L",
                        "#.#LLLL.##",
                    )
                ),
                layout,
            )

        layout, _ = simulate(layout)
        with self.subTest("iteration 3"):
            self.assertLayoutEqual(
                "\n".join(
                    (
                        "#.##.L#.##",
                        "#L###LL.L#",
                        "L.#.#..#..",
                        "#L##.##.L#",
                        "#.##.LL.LL",
                        "#.###L#.##",
                        "..#.#.....",
                        "#L######L#",
                        "#.LL###L.L",
                        "#.#L###.##",
                    )
                ),
                layout,
            )

    def test_simulate_p2(self):
        layout = layout_from_string(self.INITIAL_LAYOUT)

        layout, _ = simulate(layout, 5, count_visible_occupied_seats)
        with self.subTest("iteration 1"):
            self.assertLayoutEqual(
                "\n".join(
                    (
                        "#.##.##.##",
                        "#######.##",
                        "#.#.#..#..",
                        "####.##.##",
                        "#.##.##.##",
                        "#.#####.##",
                        "..#.#.....",
                        "##########",
                        "#.######.#",
                        "#.#####.##",
                    )
                ),
                layout,
            )

        layout, _ = simulate(layout, 5, count_visible_occupied_seats)
        with self.subTest("iteration 2"):
            self.assertLayoutEqual(
                "\n".join(
                    (
                        "#.LL.LL.L#",
                        "#LLLLLL.LL",
                        "L.L.L..L..",
                        "LLLL.LL.LL",
                        "L.LL.LL.LL",
                        "L.LLLLL.LL",
                        "..L.L.....",
                        "LLLLLLLLL#",
                        "#.LLLLLL.L",
                        "#.LLLLL.L#",
                    )
                ),
                layout,
            )

        layout, _ = simulate(layout, 5, count_visible_occupied_seats)
        with self.subTest("iteration 3"):
            self.assertLayoutEqual(
                "\n".join(
                    (
                        "#.L#.##.L#",
                        "#L#####.LL",
                        "L.#.#..#..",
                        "##L#.##.##",
                        "#.##.#L.##",
                        "#.#####.#L",
                        "..#.#.....",
                        "LLL####LL#",
                        "#.L#####.L",
                        "#.L####.L#",
                    )
                ),
                layout,
            )

        layout, _ = simulate(layout, 5, count_visible_occupied_seats)
        with self.subTest("iteration 4"):
            self.assertLayoutEqual(
                "\n".join(
                    (
                        "#.L#.L#.L#",
                        "#LLLLLL.LL",
                        "L.L.L..#..",
                        "##LL.LL.L#",
                        "L.LL.LL.L#",
                        "#.LLLLL.LL",
                        "..L.L.....",
                        "LLLLLLLLL#",
                        "#.LLLLL#.L",
                        "#.L#LL#.L#",
                    )
                ),
                layout,
            )

    def test_count_occupied_seats(self):
        final_layout = simulate_until_no_changes(
            layout_from_string(self.INITIAL_LAYOUT)
        )
        self.assertEqual(37, count_occupied_seats(final_layout))

        final_layout = simulate_until_no_changes(
            layout_from_string(self.INITIAL_LAYOUT), 5, count_visible_occupied_seats,
        )
        self.assertEqual(26, count_occupied_seats(final_layout))

    def test_count_adjacent_occupied_seats(self):
        self.assertEqual(
            0, count_adjacent_occupied_seats(layout_from_string("#"), 0, 0)
        )
        self.assertEqual(
            0, count_adjacent_occupied_seats(layout_from_string("L"), 0, 0)
        )
        data = {
            "##\nL#": [(2, 0, 0), (2, 1, 0), (3, 0, 1), (2, 1, 1)],
            "LL#\n#LL\n##L": [
                (1, 0, 0),
                (2, 1, 0),
                (0, 2, 0),
                (2, 0, 1),
                (4, 1, 1),
                (2, 2, 1),
                (2, 0, 2),
                (2, 1, 2),
                (1, 2, 2),
            ],
        }
        for layout_str, test_data in data.items():
            layout = layout_from_string(layout_str)
            for expected, x, y in test_data:
                with self.subTest(layout=layout_str, x=x, y=y):
                    self.assertEqual(
                        expected, count_adjacent_occupied_seats(layout, x, y)
                    )

    def test_count_visible_occupied_seats(self):
        data = {
            "#": [(0, 0, 0)],
            "L": [(0, 0, 0)],
            "##\nL#": [(2, 0, 0), (2, 1, 0), (3, 0, 1), (2, 1, 1)],
            "L.#\n#.L\n##L": [
                (2, 0, 0),
                (1, 2, 0),
                (2, 0, 1),
                (3, 2, 1),
                (3, 0, 2),
                (2, 1, 2),
                (1, 2, 2),
            ],
            ".......#.\n...#.....\n.#.......\n.........\n..#L....#\n....#....\n.........\n#........\n...#.....": [
                (8, 3, 4)
            ],
            "............\n.L.L.#.#.#.#.\n.............": [(0, 1, 1)],
            ".##.##.\n#.#.#.#\n##...##\n...L...\n##...##\n#.#.#.#\n.##.##.": [
                (0, 3, 3)
            ],
        }
        for layout_str, test_data in data.items():
            layout = layout_from_string(layout_str)
            for expected, x, y in test_data:
                with self.subTest(layout=layout_str, x=x, y=y):
                    self.assertEqual(
                        expected, count_visible_occupied_seats(layout, x, y)
                    )


if __name__ == "__main__":
    with open("day_11-input.txt", "r") as fh:
        initial_layout = layout_from_string(fh.read())
        final_layout = simulate_until_no_changes(initial_layout)

        part_1 = count_occupied_seats(final_layout)
        print(part_1)  # Part 1: 2412

        final_layout = simulate_until_no_changes(
            initial_layout, 5, count_visible_occupied_seats
        )
        part_2 = count_occupied_seats(final_layout)
        print(part_2)  # Part 2: 2176
