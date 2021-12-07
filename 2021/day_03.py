from pathlib import Path
from collections import defaultdict, Counter


def part1(numbers: list[str]) -> int:
    counters = defaultdict(lambda: defaultdict(int))
    for number in numbers:
        for i, bit in enumerate(number):
            counters[i][bit] += 1

    gamma_rate = int(
        "".join("1" if c["1"] >= c["0"] else "0" for c in counters.values()), 2
    )
    epsilon_rate = int(
        "".join("1" if c["1"] < c["0"] else "0" for c in counters.values()), 2
    )
    return gamma_rate * epsilon_rate


def part2(numbers: list[str]) -> int:
    o2_number = calculate_most_least(numbers, True)
    co2_number = calculate_most_least(numbers, False)
    return o2_number * co2_number


def calculate_most_least(numbers: list[str], most_least: bool):
    for index in range(len(numbers[0])):
        counter = Counter()
        for number in numbers:
            bit = number[index]
            counter[bit] += 1
        if counter["0"] == counter["1"]:
            keep = "1" if most_least else "0"
        else:
            keep = counter.most_common(2)[0 if most_least else 1][0]
        to_keep = []
        for number in numbers:
            if number[index] == keep:
                to_keep.append(number)
        numbers = to_keep
        if len(numbers) == 1:
            return int(numbers[0], 2)


if __name__ == "__main__":
    with Path(__name__).parent.joinpath("day_03-input.txt").open("r") as input_f:
        input_lines = [s.strip() for s in input_f.readlines()]
    print("Part1: ", part1(input_lines))
    print("Part2: ", part2(input_lines))
