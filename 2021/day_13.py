import re
from pathlib import Path
from typing import Optional

FOLD_REGEX = re.compile(r"fold along (?P<axis>[xy])=(?P<value>\d+)")


def print_dots(dots: set[tuple[int, int]]):
    max_x = max(d[0] for d in dots) + 1
    max_y = max(d[1] for d in dots) + 1
    for y in range(max_y):
        print("".join("##" if (x, y) in dots else ".." for x in range(max_x)))
    print()


def do_folds(
    dots: set[tuple[int, int]],
    folds: list[tuple[str, int]],
    max_folds: Optional[int] = None,
) -> set[tuple[int, int]]:
    for fold_count, (axis, value) in enumerate(folds):
        if max_folds is not None and fold_count >= max_folds:
            break
        folded_dots: set[tuple[int, int]] = set()
        for x, y in dots:
            if axis == "y" and y >= value:
                folded_dots.add((x, 2 * value - y))
            elif axis == "x" and x >= value:
                folded_dots.add((2 * value - x, y))
            else:
                folded_dots.add((x, y))
        dots = folded_dots
    return dots


def main():
    dots: set[tuple[int, int]] = set()
    folds: list[tuple[str, int]] = []
    with Path(__file__).parent.joinpath("day_13-input.txt").open("r") as input_f:
        for line in input_f:
            if not line.strip():
                break
            x, y = line.strip().split(",")
            dots.add((int(x), int(y)))
        for line in input_f:
            if matches := FOLD_REGEX.match(line):
                folds.append((matches["axis"], int(matches["value"])))

    print("Part1: ", len(do_folds(dots, folds, None)))
    print("Part2: ↓")
    print_dots(do_folds(dots, folds))


if __name__ == "__main__":
    main()
