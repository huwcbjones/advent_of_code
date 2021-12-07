from __future__ import annotations

from pathlib import Path

_Grid = list[list[int]]
_Matches: list[list[bool]]


class Board:
    MATCH = [True] * 5

    def __init__(self, grid: _Grid):
        self._grid = grid
        self._matches: _Matches = [[False] * len(c) for c in grid]

    def has_match(self) -> bool:
        # check horizontal
        if any(r == self.MATCH for r in self._matches):
            return True

        # check vertical
        if any([r[i] for r in self._matches] == self.MATCH for i in range(5)):
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
        return "\n".join(
            " ".join(
                ("*" if self._matches[y][x] else " ") + f"{i:2}"
                for x, i in enumerate(row)
            )
            for y, row in enumerate(self._grid)
        )


def part1(numbers, boards) -> int | None:
    for turn, number in enumerate(numbers):
        matching_boards = set()
        for board in boards:
            if board.match(number):
                matching_boards.add(board)
        if matching_boards:
            for board in matching_boards:
                return board.score(number)
    return None


def part2(numbers, boards) -> int:
    completed_boards: set[Board] = set()
    winning_boards: list[tuple[Board, int]] = []
    for turn, number in enumerate(numbers):
        for board in boards:
            if board not in completed_boards and board.match(number):
                completed_boards.add(board)
                winning_boards.append((board, number))

    return winning_boards[-1][0].score(winning_boards[-1][1])


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
    print("Part1: ", part1(numbers, boards))
    print("Part2: ", part2(numbers, boards))


if __name__ == "__main__":
    main()
