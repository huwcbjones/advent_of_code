from __future__ import annotations

import math
import re
from pathlib import Path
from typing import Iterable


def triangular_number(n) -> int:
    return (n * (n + 1)) // 2


def triangular_root(n) -> float:
    return (math.sqrt(8 * n + 1) - 1) / 2


def simulate(
    start_v: tuple[int, int],
    x_range: tuple[int, int],
    y_range: tuple[int, int],
):
    max_height = 0
    x, y = 0, 0
    v_x, v_y = start_v

    while not (x_range[0] <= x <= x_range[1] and y_range[0] <= y <= y_range[1]):
        x += v_x
        y += v_y
        if x > x_range[1] or y < y_range[0]:
            raise Exception()
        max_height = max(max_height, y)
        if v_x != 0:  # drag
            v_x -= int(math.copysign(1, v_x))
        v_y -= 1  # gravity
        # print(f"({x}, {y}) [{v_x}, {v_y}]")
    return max_height


def find_min_x(x_range: tuple[int, int]) -> int:
    min_x = math.floor(triangular_root(x_range[0]))
    while not (x_range[0] <= triangular_number(min_x) <= x_range[1]):
        min_x += 1
    return min_x


def part1(y_range: tuple[int, int]) -> int:
    return triangular_number(max_y(y_range))


def max_y(y_range: tuple[int, int]) -> int:
    return abs(min(y_range)) - 1


def part2(x_range: tuple[int, int], y_range: tuple[int, int]) -> int:
    velocities: set[tuple[int, int]] = set()
    start_y = max_y(y_range)
    end_y = min(y_range) - 1

    for x, steps in find_all_x(x_range):
        for y in range(start_y, end_y, -1):
            try:
                simulate((x, y), x_range, y_range)
                velocities.add((x, y))
            except Exception:
                pass
    return len(velocities)


def find_all_x(x_range: tuple[int, int]) -> Iterable[tuple[int, int]]:
    for x in range(find_min_x(x_range), max(x_range) + 1):
        position = 0
        for i, c in enumerate(range(x, 1, -1), 1):
            position += c
            if x_range[0] <= position <= x_range[1]:
                yield x, i
                break


def main():
    with Path(__file__).parent.joinpath("day_17-input.txt").open("r") as input_f:
        if matches := re.match(
            r"target area: x=(?P<x1>-?\d+)..(?P<x2>-?\d+), y=(?P<y1>-?\d+)..(?P<y2>-?\d+)",
            input_f.readline().strip(),
        ):
            x1 = int(matches["x1"])
            x2 = int(matches["x2"])
            y1 = int(matches["y1"])
            y2 = int(matches["y2"])
            x_range = (min(x1, x2), max(x1, x2))
            y_range = (min(y1, y2), max(y1, y2))

    p1 = part1(y_range)
    assert p1 == 5671, p1
    print("Part1: ", p1)

    p2 = part2(x_range, y_range)
    assert p2 == 4556
    print("Part2: ", p2)


if __name__ == "__main__":
    main()
