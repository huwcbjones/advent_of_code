from collections import Counter, defaultdict
from itertools import pairwise
from pathlib import Path


def run_polymerase(polymer: str, rules: dict[str, str], steps: int = 1) -> int:
    pairs = dict(Counter(pairwise(polymer)).most_common())
    for s in range(steps):
        new_pairs = defaultdict(int)
        for (l, r), total in pairs.items():
            if i := rules.get(f"{l}{r}", ""):
                new_pairs[f"{l}{i}"] += total
                new_pairs[f"{i}{r}"] += total
            else:
                new_pairs[f"{l}{r}"] += total
        pairs = new_pairs

    counter = Counter()
    counter[polymer[0]] += 1
    counter[polymer[-1]] += 1
    for (l, r), total in pairs.items():
        counter[l] += total
        counter[r] += total
    counts = counter.most_common()
    return (counts[0][1] - counts[-1][1]) // 2


def main():
    rules: dict[str, str] = {}
    with Path(__file__).parent.joinpath("day_14-input.txt").open("r") as input_f:
        template = input_f.readline().strip()
        for line in input_f.readlines():
            if not line.strip():
                continue
            pair, insert = line.strip().split(" -> ")
            rules[pair] = insert

    print("Part1: ", run_polymerase(template, rules, 10))
    print("Part2: ", run_polymerase(template, rules, 40))


if __name__ == "__main__":
    main()
