from __future__ import annotations

from pathlib import Path


class Board:
    MATCH = [True] * 5

    def __init__(self, grid: list[list[int]]):
        self._grid = grid
        self._matches: list[list[bool]] = [[False] * len(c) for c in grid]

    def has_match(self) -> bool:
        if any(r == self.MATCH for r in self._matches):
            # horizontal
            return True
        if any([r[i] for r in self._matches] == self.MATCH for i in range(5)):
            # vertical
            return True
        return False

    def match(self, number: int) -> bool:
        for y, row in enumerate(self._grid):
            for x, i in enumerate(row):
                if i == number:
                    self._matches[y][x] = True
        return self.has_match()

    def score(self, winning_number: int) -> int:
        unmarked = 0
        for y, row in enumerate(self._grid):
            for x, i in enumerate(row):
                if not self._matches[y][x]:
                    unmarked += i
        return unmarked * winning_number

    def __str__(self):
        return "\n".join(" ".join(("*" if self._matches[y][x] else " ") + f"{i:2}" for x, i in enumerate(row)) for y, row in enumerate(self._grid))


def part1(numbers, boards):
    for t, number in enumerate(numbers):
        matching_boards = set()
        print(f"TURN {t + 1}: {number}")
        for board in boards:
            if board.match(number):
                matching_boards.add(board)
        if matching_boards:
            print("WE HAVE A MATCH!")
            for board in matching_boards:
                print(board)
                print(board.score(number))
            break


def part2(numbers, boards):
    completed_boards: set[Board] = set()
    winning_boards: list[tuple[Board, int]] = []
    for t, number in enumerate(numbers):
        print(f"TURN {t + 1}: {number}")
        for board in boards:
            if board not in completed_boards and board.match(number):
                completed_boards.add(board)
                winning_boards.append((board, number))
    print(winning_boards[-1][0].score(winning_boards[-1][1]))


def parse_input() -> tuple[list[int], list[Board]]:
    with Path(__name__).parent.joinpath("day_04-input.txt").open("r") as input_f:
        numbers = [int(i) for i in input_f.readline().split(",")]
        boards = []
        board = []
        for line in input_f.readlines():
            if line == "\n":
                if board:
                    boards.append(Board(board))
                board = []
                continue
            board.append([int(i) for i in line.strip().split(" ") if i])
        if board:
            boards.append(Board(board))
    return numbers, boards


def main():
    numbers, boards = parse_input()
    # part1(numbers, boards)
    part2(numbers, boards)


if __name__ == "__main__":
    main()
