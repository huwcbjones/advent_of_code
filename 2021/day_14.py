from collections import Counter
from itertools import pairwise
from pathlib import Path


def polymerase(polymer: str, rules: dict[str, str]) -> str:
    insertions: dict[int, str] = {}
    index = 0
    for pair in pairwise(polymer):
        index += 1
        if insertion := rules.get(f"{pair[0]}{pair[1]}", ""):
            insertions[index] = insertion
    new_polymer = list(polymer)
    for index, insertion in sorted(insertions.items(), reverse=True):
        new_polymer.insert(index, insertion)
    return "".join(new_polymer)


def run_polymerase(polymer: str, rules: dict[str, str], steps: int = 1) -> str:
    for i in range(steps):
        polymer = polymerase(polymer, rules)
        # print(f"After step {i + 1}: {polymer}")
    return polymer


def part1(polymer: str) -> int:
    counts = Counter(polymer).most_common()
    return counts[0][1] - counts[-1][1]


def main():
    rules: dict[str, str] = {}
    with Path(__file__).parent.joinpath("day_14-input.txt").open("r") as input_f:
        template = input_f.readline().strip()
        for line in input_f.readlines():
            if not line.strip():
                continue
            pair, insert = line.strip().split(" -> ")
            rules[pair] = insert

    polymer = run_polymerase(template, rules, 10)
    print("Part1: ", part1(polymer))


if __name__ == "__main__":
    main()
