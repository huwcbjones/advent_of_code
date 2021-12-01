from collections import deque
from pathlib import Path


def part1():
    previous_depth = None
    depth_changes = 0
    with Path(__name__).parent.joinpath("day_01-input.txt").open("r") as report:
        for line in report.readlines():
            depth = int(line)
            if previous_depth is not None and depth > previous_depth:
                depth_changes += 1
            previous_depth = depth
    print(depth_changes)


def part2():
    depths = deque(maxlen=3)
    depth_changes = 0
    with Path(__name__).parent.joinpath("day_01-input.txt").open("r") as report:
        for line in report.readlines():
            depth = int(line)

            depth_count = len(depths)
            previous_depth = sum(depths)
            depths.append(depth)

            if depth_count == 3 and sum(depths) > previous_depth:
                depth_changes += 1
    print(depth_changes)


if __name__ == "__main__":
    part2()
