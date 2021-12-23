from __future__ import annotations

import math
import re
from pathlib import Path


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
        max_height = max(max_height, y)
        if v_x != 0:  # drag
            v_x -= int(math.copysign(1, v_x))
        v_y -= 1  # gravity
        # print(f"({x}, {y}) [{v_x}, {v_y}]")
    return max_height


def part1(x_range: tuple[int, int], y_range: tuple[int, int]) -> int:
    v_x: int | None = None
    for i in range(
        math.floor(triangular_root(x_range[0])), math.ceil(triangular_root(x_range[1]))
    ):
        if x_range[0] <= triangular_number(i) <= x_range[1]:
            v_x = i
            break
    v_y = abs(min(y_range)) - 1
    print(f"Optimal Values: ({v_x}, {v_y})")
    return simulate((v_x, v_y), x_range, y_range)


def main():
    with Path(__file__).parent.joinpath("day_17-example.txt").open("r") as input_f:
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

    print("Part1: ", part1(x_range, y_range))


if __name__ == "__main__":
    main()
