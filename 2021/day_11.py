from copy import deepcopy
from pathlib import Path
from itertools import product
from collections import deque


def format_grid(grid):
    return "\n".join(
        " ".join(f"{grid[y][x]: >2d}" for x, i in row.items())
        for y, row in grid.items()
    )


def run_simulation(grid: dict[int, dict[int, int]], steps: int = 100) -> int:
    octupi_count = sum(len(r) for r in grid.values())
    flash_count = 0
    step = 0
    while steps == -1 or step < steps:
        flashed: set[tuple[int, int]] = set()

        # Stage 1, increment all energy levels
        for y, row in grid.items():
            for x in row:
                grid[y][x] += 1

        # Stage 2, flash and increment until all have flashed
        to_check: set[tuple[int, int]] = deque(
            {(x, y) for y, r in grid.items() for x in r if grid[y][x] > 9}
        )
        while to_check:
            x, y = to_check.pop()
            if (x, y) in flashed:
                continue
            if grid[y][x] <= 9:
                continue
            flashed.add((x, y))
            for d_x, d_y in product(iter([-1, 0, 1]), repeat=2):
                p_x, p_y = (x + d_x, y + d_y)
                if (d_x, d_y) == (0, 0) or (p_x, p_y) in flashed:
                    continue
                try:
                    grid[p_y][p_x] += 1
                    if grid[p_y][p_x] > 9:
                        to_check.append((p_x, p_y))
                except KeyError:
                    pass
        flash_count += len(flashed)

        # Stage 3: reset flashed to 0
        for x, y in flashed:
            grid[y][x] = 0

        step += 1
        if steps == -1 and len(flashed) == octupi_count:
            return step

    return flash_count


def main():
    with Path(__file__).parent.joinpath("day_11-input.txt").open("r") as input_f:
        grid = {
            y: {x: int(i) for x, i in enumerate(row.strip())}
            for y, row in enumerate(input_f.readlines())
        }
    print("Part1: ", run_simulation(deepcopy(grid)))
    print("Part2: ", run_simulation(deepcopy(grid), -1))


if __name__ == "__main__":
    main()
