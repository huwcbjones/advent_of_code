from pathlib import Path
from collections import deque, Counter


ERROR_POINTS: dict[str, int] = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}
INCOMPLETE_POINTS: dict[str, int] = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}
OPENERS = {"(": ")", "[": "]", "{": "}", "<": ">"}


def score_errors(lines: list[str]) -> int:
    errors = Counter()
    for line in lines:
        stack = deque()
        for char in line:
            if char in OPENERS:
                stack.append(char)
                continue
            opener = stack.pop()
            if OPENERS[opener] != char:
                errors[char] += 1
                break
    return sum(ERROR_POINTS[k] * c for k, c in errors.items())


def score_incomplete(lines: list[str]) -> int:
    scores: list[int] = []
    for line in lines:
        stack = deque()
        for char in line:
            if char in OPENERS:
                stack.append(char)
                continue
            opener = stack.pop()
            if OPENERS[opener] != char:
                break
        else:
            score = 0
            while stack:
                score *= 5
                score += INCOMPLETE_POINTS[OPENERS[stack.pop()]]
            scores.append(score)
    scores.sort()
    return scores[len(scores) // 2]


def main():
    with Path(__file__).parent.joinpath("day_10-input.txt").open("r") as input_f:
        lines: list[str] = [i.strip() for i in input_f.readlines()]

    print("Part1: ", score_errors(lines))
    print("Part2: ", score_incomplete(lines))


if __name__ == "__main__":
    main()
