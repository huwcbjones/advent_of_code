import logging
from functools import lru_cache
from typing import List, Tuple, Optional, Dict, Set, NamedTuple, Union


class CoOrd(NamedTuple):
    x: int
    y: int

    def __add__(self, other) -> "CoOrd":
        if isinstance(other, self.__class__):
            return CoOrd(self.x + other.x, self.y + other.y)
        if isinstance(other, tuple):
            return CoOrd(self.x + other[0], self.y + other[1])

        raise TypeError(
            "TypeError: unsupported operand type(s) for +: '{}' and '{}'".format(
                type(self).__name__, type(other).__name__
            )
        )

    def __str__(self):
        return f"({self.x}, {self.y})"


class AsteroidField:
    def __init__(self, asteroid_map: str) -> None:
        self._map = asteroid_map.strip()
        self._data: List[List[str]] = [
            [c for c in row] for row in self._map.split("\n")
        ]
        self.height = len(self._data)
        self.width = len(self._data[0])
        self._asteroids: Dict[CoOrd, Optional[int]] = {}

        for y, row in enumerate(self._data):
            for x in range(0, len(row)):
                if row[x] == "#":
                    self._asteroids[CoOrd(x, y)] = None
        self._count_asteroids()

    def _count_asteroids(self):
        for co_ord in self._asteroids.keys():
            logging.info("Finding asteroids visible from %s", co_ord)
            visible = self._count_visible_asteroids(co_ord)
            logging.info("Number of asteroids visible from %s: %s\n", co_ord, visible)
            self._asteroids[co_ord] = visible

    def _count_visible_asteroids(self, target: CoOrd) -> int:
        visible_asteroids: Set[CoOrd] = set()

        for asteroid in self._asteroids.keys():
            # Ignore current asteroid
            if asteroid.x == target.x and asteroid.y == target.y:
                logging.debug(f"Checking asteroid %s: IGN", asteroid)
                continue
            possible_locations = self._get_possible_asteroids_coords(target, asteroid)
            is_blocked: bool = True
            for poss in possible_locations:
                if poss not in self._asteroids.keys():
                    continue
                if poss == asteroid:
                    is_blocked = False
                break
            if not is_blocked:
                logging.debug(f"Checking asteroid %s: VIS", asteroid)
                visible_asteroids.add(asteroid)
            else:
                logging.debug(f"Checking asteroid %s: BLK", asteroid)

        return len(visible_asteroids)

    def _get_possible_asteroids_coords(self, source: CoOrd, target: CoOrd):
        d_x = target.x - source.x
        d_y = target.y - source.y
        delta = get_smallest_int_delta(d_x, d_y)

        target: CoOrd = source + delta
        possible_locations: List[CoOrd] = []
        while 0 <= target.x < self.width and 0 <= target.y < self.height:
            possible_locations.append(target)
            target += delta
        return possible_locations

    def get_best_monitoring_position(self) -> CoOrd:
        return sorted(
            [(k, v) for k, v in self._asteroids.items()],
            key=lambda x: x[1],
            reverse=True,
        )[0][0]

    def get_visible_asteroid_count(self, position: CoOrd):
        return self._asteroids[position]


@lru_cache
def get_smallest_int_delta(
    x: Union[int, float], y: Union[int, float]
) -> Tuple[int, int]:
    gcd = abs(get_greatest_common_divider(x, y))
    return int(x / gcd), int(y / gcd)


@lru_cache
def get_greatest_common_divider(x, y):
    while y:
        x, y = y, x % y

    return x


def test1():
    field = AsteroidField(
        """.#..#
.....
#####
....#
...##
"""
    )
    assert (3, 4) == field.get_best_monitoring_position()


def test2():
    field = AsteroidField(
        """......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####
"""
    )
    assert (5, 8) == field.get_best_monitoring_position()


def test3():
    field = AsteroidField(
        """#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###.
"""
    )
    assert (1, 2) == field.get_best_monitoring_position()


def part1():
    with open("day_10-input.txt", "r") as f:
        field = AsteroidField(f.read())
    best_position = field.get_best_monitoring_position()
    print(field.get_visible_asteroid_count(best_position))


if __name__ == "__main__":
    # test1()
    # test2()
    # test3()
    part1()
