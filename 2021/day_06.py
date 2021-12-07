from collections import defaultdict
from pathlib import Path


def calculate_number_of_fish(state: dict[int, int], days: int) -> int:
    for i in range(days):
        state = {k - 1: v for k, v in state.items()}
        if reproduce_count := state.pop(-1, 0):
            state[6] = state.get(6, 0) + reproduce_count
            state[8] = state.get(8, 0) + reproduce_count
    return sum(state.values())


def main():
    days_to_fish: dict[int, int] = defaultdict(int)
    with Path(__file__).parent.joinpath("day_06-input.txt").open("r") as input_f:
        for c in input_f.readline().split(","):
            days_to_fish[int(c)] += 1

    print("Part1: ", calculate_number_of_fish(days_to_fish, 80))
    print("Part2: ", calculate_number_of_fish(days_to_fish, 256))


if __name__ == "__main__":
    main()
