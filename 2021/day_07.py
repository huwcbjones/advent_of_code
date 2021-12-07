from collections import defaultdict
from pathlib import Path
from typing import Callable


def calculate_fuel(positions: dict[int, int], fuel_calc: Callable[[int], int]) -> int:
    return min(
        {
            i: sum(fuel_calc(abs(pos - i)) * count for pos, count in positions.items())
            for i in range(min(positions.keys()), max(positions.keys()) + 1)
        }.values()
    )


def main():
    positions: dict[int, int] = defaultdict(int)
    with Path(__file__).parent.joinpath("day_07-input.txt").open("r") as input_f:
        for c in input_f.readline().split(","):
            positions[int(c)] += 1

    print("Part1: ", calculate_fuel(positions, lambda n: n))
    print("Part2: ", calculate_fuel(positions, lambda n: n * (n + 1) // 2))


if __name__ == "__main__":
    main()
