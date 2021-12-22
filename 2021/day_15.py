from __future__ import annotations

from functools import cached_property, total_ordering
from pathlib import Path
from queue import PriorityQueue
from typing import Iterable


def print_grid(grid: Grid):
    for y in range(grid.max_y + 1):
        print("".join(str(grid.get_risk(x, y)) for x in range(grid.max_x + 1)))


@total_ordering
class Route:
    def __init__(self, nodes: list[tuple[int, int]], grid: Grid):
        self._nodes = nodes
        self._grid = grid

    @cached_property
    def end(self) -> tuple[int, int]:
        return self._nodes[-1]

    @cached_property
    def x(self) -> int:
        return self.end[0]

    @cached_property
    def y(self) -> int:
        return self.end[1]

    @cached_property
    def risk(self) -> int:
        if len(self._nodes) <= 1:
            return 0
        return sum(self._grid.get_risk(x, y) for x, y in self._nodes[1:])

    @cached_property
    def priority(self) -> int:
        closeness = (self._grid.max_x - self.x) + (self._grid.max_y - self.y)
        return self.risk + closeness + len(self._nodes)

    @cached_property
    def is_complete(self) -> bool:
        return self.x == self._grid.max_x and self.y == self._grid.max_y

    @cached_property
    def neighbours(self) -> Iterable[Route]:
        x, y = self.end
        for d_x, d_y in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            if (d_x, d_y) == (0, 0):
                continue
            p_x, p_y = (x + d_x, y + d_y)
            if 0 <= p_x <= self._grid.max_x and 0 <= p_y <= self._grid.max_y:
                yield Route(self._nodes + [(p_x, p_y)], self._grid)

    def __contains__(self, item):
        return item in self._nodes

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self._nodes == other._nodes

    def __lt__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.priority < other.priority

    def __hash__(self):
        return hash(tuple(self._nodes))

    def __repr__(self):
        return f"Route<{self.priority}: {self._nodes}>"


class Grid(list[list[int]]):
    def __init__(self, *args, repeat: int = 1, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.repeat = repeat
        self.height = len(self)
        self.width = max(len(r) for r in self)

    @property
    def max_y(self) -> int:
        return (self.height * self.repeat) - 1

    @property
    def max_x(self) -> int:
        return (self.width * self.repeat) - 1

    def get_risk(self, x: int, y: int) -> int:
        m_x, i_x = divmod(x, self.width)
        m_y, i_y = divmod(y, self.height)
        if m_x > self.repeat or m_y > self.repeat:
            raise IndexError((x, y))
        val = self[i_y][i_x] + (m_x + m_y)
        if val > 9:
            return val % 9
        return val


def pathfind(grid: Grid) -> Route:
    seen: set[tuple[int, int]] = set()
    routes: PriorityQueue[Route] = PriorityQueue()
    routes.put(Route([(0, 0)], grid))

    while routes.qsize():
        route = routes.get()

        if route.is_complete:
            return route

        if route.end in seen:
            continue
        seen.add(route.end)

        for next_route in route.neighbours:
            if next_route.end in seen:
                continue
            routes.put(next_route)


def main():
    with Path(__file__).parent.joinpath("day_15-input.txt").open("r") as input_f:
        grid: Grid = Grid(
            [[int(x) for x in line.strip()] for line in input_f.readlines()]
        )

    route = pathfind(grid)
    print("Part1: ", route.risk)
    grid.repeat = 5
    route = pathfind(grid)
    print("Part2: ", route.risk)


if __name__ == "__main__":
    main()
