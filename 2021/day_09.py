from functools import reduce
from pathlib import Path


def get_adjacent_points(
    heightmap: dict[int, dict[int, int]], x: int, y: int
) -> list[tuple[int, int]]:
    adjacent_points: list[tuple[int, int]] = []
    for dx in [-1, 1]:
        try:
            _ = heightmap[y][x + dx]
            adjacent_points.append((x + dx, y))
        except KeyError:
            pass
    for dy in [-1, 1]:
        try:
            _ = heightmap[y + dy][x]
            adjacent_points.append((x, y + dy))
        except KeyError:
            pass
    return adjacent_points


def find_low_points(heightmap: dict[int, dict[int, int]]) -> dict[tuple[int, int], int]:
    low_points: dict[tuple[int, int], int] = {}
    for y, row in heightmap.items():
        for x, height in row.items():
            adjacent_points = get_adjacent_points(heightmap, x, y)
            if height < min(heightmap[y][x] for x, y in adjacent_points):
                low_points[(x, y)] = height
    return low_points


def find_largest_three_basins(
    heightmap: dict[int, dict[int, int]], low_points: dict[tuple[int, int], int]
) -> int:
    basins: list[int] = []
    for low_point, height in low_points.items():
        checked_points: set[tuple[int, int]] = {low_point}
        points_to_check: set[tuple[int, int, int]] = {
            p + (height,) for p in get_adjacent_points(heightmap, *low_point)
        }
        while points_to_check:
            x, y, compare_height = points_to_check.pop()
            height = heightmap[y][x]
            if compare_height <= height < 9:
                checked_points.add((x, y))
                for adjacent_point in get_adjacent_points(heightmap, x, y):
                    if adjacent_point not in checked_points:
                        points_to_check.add(adjacent_point + (height,))
        basins.append(len(checked_points))
    basins.sort(reverse=True)
    return reduce(lambda v, e: v * e, basins[:3])


def main():
    with Path(__file__).parent.joinpath("day_09-input.txt").open("r") as input_f:
        heightmap = {
            y: {x: int(i) for x, i in enumerate(r.strip())}
            for y, r in enumerate(input_f.readlines())
            if r.strip()
        }
    low_points = find_low_points(heightmap)
    print("Part1: ", sum(lp + 1 for lp in low_points.values()))
    print("Part2: ", find_largest_three_basins(heightmap, low_points))


if __name__ == "__main__":
    main()
