from collections import deque
from pathlib import Path


def part1(depths: list[int]):
    previous_depth = None
    depth_changes = 0
    for depth in depths:
        if previous_depth is not None and depth > previous_depth:
            depth_changes += 1
        previous_depth = depth
    return depth_changes


def part2(depths: list[int]):
    depth_queue = deque(maxlen=3)
    depth_changes = 0
    for depth in depths:
        previous_depth = sum(depth_queue)
        depth_queue.append(depth)

        if len(depth_queue) == 3 and sum(depth_queue) > previous_depth:
            depth_changes += 1
    return depth_changes


def main():
    with Path(__name__).parent.joinpath("day_01-input.txt").open("r") as report:
        depths = [int(i) for i in report.readlines()]
        print("Part1: ", part1(depths))
        print("Part2: ", part2(depths))


if __name__ == "__main__":
    main()
