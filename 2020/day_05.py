from math import floor
from typing import Iterable, List
from unittest import TestCase


def get_row(seat: str) -> int:
    upper = 128
    lower = 0
    for i in seat[:7]:
        if i == "F":
            upper = floor((upper + lower) / 2)
        elif i == "B":
            lower = floor((upper + lower) / 2)
    return lower


def get_col(seat: str) -> int:
    upper = 8
    lower = 0
    for i in seat[7:]:
        if i == "L":
            upper = floor((upper + lower) / 2)
        elif i == "R":
            lower = floor((upper + lower) / 2)
    return lower


def get_seat_id(seat: str) -> int:
    return get_row(seat) * 8 + get_col(seat)


def find_spare_seats(seats: List[int]) -> List[int]:
    previous_seat = None
    spare_seats = []
    for i in range(0 * 8 + 0, 127 * 8 + 7 + 1):
        if i in seats:
            previous_seat = i
            continue
        if previous_seat is not None and i - 1 == previous_seat and (i + 1) in seats:
            spare_seats.append(i)
    return spare_seats


class Day05Test(TestCase):
    def test_get_row(self):
        self.assertEqual(44, get_row("FBFBBFFRLR"))
        self.assertEqual(70, get_row("BFFFBBFRRR"))
        self.assertEqual(14, get_row("FFFBBBFRRR"))
        self.assertEqual(102, get_row("BBFFBBFRLL"))

    def test_get_col(self):
        self.assertEqual(5, get_col("FBFBBFFRLR"))
        self.assertEqual(7, get_col("BFFFBBFRRR"))
        self.assertEqual(7, get_col("FFFBBBFRRR"))
        self.assertEqual(4, get_col("BBFFBBFRLL"))

    def test_get_seat_id(self):
        self.assertEqual(357, get_seat_id("FBFBBFFRLR"))
        self.assertEqual(567, get_seat_id("BFFFBBFRRR"))
        self.assertEqual(119, get_seat_id("FFFBBBFRRR"))
        self.assertEqual(820, get_seat_id("BBFFBBFRLL"))


if __name__ == "__main__":
    with open("day_05-input.txt", "r") as fh:
        seat_ids = sorted([get_seat_id(s) for s in fh if s.strip()])
        part_1 = seat_ids[-1]  # max(seat_ids)
        print(part_1)  # Part 1: 991

        part_2 = find_spare_seats(seat_ids)
        print(part_2[0])  # Part 2: 534
