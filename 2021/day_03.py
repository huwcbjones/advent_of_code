from pathlib import Path
from collections import defaultdict, Counter


def part1(numbers):
    counters = defaultdict(Counter)
    for number in numbers:
        for i, bit in enumerate(number):
            if bit != "\n":
                counters[i][bit] += 1

    gamma_rate = int("".join(c.most_common(1)[0][0] for c in counters.values()), 2)
    epsilon_rate = int("".join(c.most_common(2)[1][0] for c in counters.values()), 2)
    print(gamma_rate * epsilon_rate)

def part2(numbers):
    o2_number = foo(numbers, True)
    co2_number = foo(numbers, False)
    print(o2_number * co2_number)

def foo(numbers, most_least):
    index = 0
    for index in range(len(numbers[0])):
        counter = Counter()
        for number in numbers:
            bit = number[index]
            if bit != "\n":
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
        input_lines = input_f.readlines()
    part1(input_lines)
    part2(input_lines)
