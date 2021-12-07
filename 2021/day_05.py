import re
from collections import defaultdict
from pathlib import Path
from typing import NamedTuple


class Coord(NamedTuple):
    x: int
    y: int

    def __str__(self) -> str:
        return f"{self.x},{self.y}"

    __repr__ = __str__

    def __add__(self, other: "Coord") -> "Coord":
        return Coord(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Coord") -> "Coord":
        return Coord(self.x - other.x, self.y - other.y)

    def __floordiv__(self, other: int) -> "Coord":
        return Coord(self.x // other, self.y // other)

    def __mul__(self, other: int) -> "Coord":
        return Coord(self.x * other, self.y * other)


class Line(NamedTuple):
    start: Coord
    end: Coord

    def __str__(self) -> str:
        return f"{self.start} -> {self.end}"

    __repr__ = __str__


Overlaps = dict[Coord, int]


def format_overlaps(overlaps: Overlaps) -> str:
    grid = "\n"
    max_x = max(c.x for c in overlaps)
    max_y = max(c.y for c in overlaps)
    for y in range(0, max_y + 1):
        for x in range(0, max_x + 1):
            count = overlaps[Coord(x, y)]
            grid += str(count) if count else "."
        grid += "\n"
    return grid


def calculate_overlaps(segments: list[Line], diagonals: bool = False) -> Overlaps:
    overlaps: dict[Coord, int] = defaultdict(int)
    for line in segments:
        if line.start.x == line.end.x:
            for y in range(
                min(line.start.y, line.end.y),
                max(line.start.y, line.end.y) + 1,
            ):
                overlaps[Coord(line.start.x, y)] += 1
        if line.start.y == line.end.y:
            for x in range(
                min(line.start.x, line.end.x),
                max(line.start.x, line.end.x) + 1,
            ):
                overlaps[Coord(x, line.start.y)] += 1
        if not diagonals:
            continue

        diff = line.end - line.start
        if abs(diff.x) == abs(diff.y) and diff.x != 0:
            step = diff // abs(diff.x)
            for i in range(0, abs(diff.x) + 1):
                overlaps[line.start + step * i] += 1
    return overlaps


def sum_overlaps(overlaps: Overlaps, threshold: int = 1) -> int:
    return sum(1 if c > threshold else 0 for c in overlaps.values())


FORMAT = re.compile(r"(?P<x1>\d+),(?P<y1>\d+) -> (?P<x2>\d+),(?P<y2>\d+)")


def main():
    segments: list[Line] = []
    with Path(__file__).parent.joinpath("day_05-input.txt").open("r") as input_f:
        for line in input_f.readlines():
            if match := FORMAT.match(line):
                line = Line(
                    Coord(int(match["x1"]), int(match["y1"])),
                    Coord(int(match["x2"]), int(match["y2"])),
                )
                segments.append(line)

    overlaps = calculate_overlaps(segments)
    # print(format_overlaps(overlaps))
    print("Part1: ", sum_overlaps(overlaps))

    overlaps = calculate_overlaps(segments, True)
    # print(format_overlaps(overlaps))
    print("Part2: ", sum_overlaps(overlaps))


if __name__ == "__main__":
    main()
