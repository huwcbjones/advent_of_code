import time
from dataclasses import dataclass
from itertools import combinations
from math import floor
from typing import NamedTuple, Tuple, List, Iterable, Optional


class Vector(NamedTuple):
    x: int = 0
    y: int = 0
    z: int = 0

    def __add__(self, other: Tuple[int, int, int]) -> "Vector":
        if not isinstance(other, tuple) and len(other) != 3:
            raise TypeError(
                "TypeError: unsupported operand type(s) for +: '{}' and '{}'".format(
                    type(self).__name__, type(other).__name__
                )
            )

        return Vector(self.x + other[0], self.y + other[1], self.z + other[2])

    def __sub__(self, other: Tuple[int, int, int]) -> "Vector":
        if not isinstance(other, tuple) and len(other) != 3:
            raise TypeError(
                "TypeError: unsupported operand type(s) for +: '{}' and '{}'".format(
                    type(self).__name__, type(other).__name__
                )
            )

        return Vector(self.x - other[0], self.y - other[1], self.z - other[2])

    @staticmethod
    def origin() -> "Vector":
        return Vector(0, 0, 0)

    def __str__(self) -> str:
        return f"<x={self.x:>3}, y={self.y:>3}, z={self.z:>3}>"


@dataclass
class Satellite:

    name: str
    position: Vector
    velocity: Vector

    def __str__(self) -> str:
        return f"{self.name:<10} pos={self.position} vel={self.velocity}"

    def clone(self) -> "Satellite":
        return Satellite(self.name, self.position, self.velocity)

    def __hash__(self) -> int:
        return (
            self.name.__hash__() + self.position.__hash__() + self.velocity.__hash__()
        )


def compare(a: int, b: int) -> int:
    if a == b:
        return 0
    if a < b:
        return 1
    return -1


def _apply_gravity(moons: Iterable[Satellite], axis: Optional[List[str]] = None):
    if axis is None:
        axis = ["x", "y", "z"]
    for a, b in combinations(moons, r=2):
        _apply_gravity_to_pair(a, b, axis)


def _apply_gravity_to_pair(a: Satellite, b: Satellite, axis: List[str]):
    x, y, z = 0, 0, 0
    if "x" in axis:
        x = compare(a.position.x, b.position.x)
    if "y" in axis:
        y = compare(a.position.y, b.position.y)
    if "z" in axis:
        z = compare(a.position.z, b.position.z)

    vector = (x, y, z)

    a.velocity += vector
    b.velocity -= vector


def _apply_velocity(moons: Iterable[Satellite]):
    for moon in moons:
        moon.position += moon.velocity


def calculate_kinetic_energy(moon: Satellite) -> int:
    return sum([abs(moon.velocity[i]) for i in range(0, 3)])


def calculate_potential_energy(moon: Satellite) -> int:
    return sum([abs(moon.position[i]) for i in range(0, 3)])


def calculate_energy(moon: Satellite) -> int:
    pot = calculate_potential_energy(moon)
    kin = calculate_kinetic_energy(moon)
    total = pot * kin
    return total


def do_tick(moons: Iterable[Satellite], axis: Optional[List[str]] = None):
    _apply_gravity(moons, axis)
    _apply_velocity(moons)


def gcf(a: int, b: int) -> int:
    a = abs(a)
    b = abs(b)
    while b:
        a, b = b, a % b

    return a


def lcm(*values: int) -> int:
    if len(values) == 1:
        return values[0]
    a = values[0]
    b = values[1]
    result = floor(a * b / gcf(a, b))
    if len(values) == 2:
        return result
    return lcm(result, *values[2:])


def find_period(moons: List[Satellite], axis: str) -> int:
    start_state = [m.clone() for m in moons]
    counter = 0

    start = time.monotonic()
    while True:
        do_tick(moons, [axis])
        counter += 1
        if counter % 1000 == 0:
            time_taken = time.monotonic() - start
            taken = "{:0>2}:{:0>2.0f}".format(floor(time_taken / 60), time_taken % 60)
            print(f"\rProcessed {counter:>10} ticks in {taken}", end="")

        if moons == start_state:
            print()
            break

    return counter


def main():
    moons = [
        Satellite("Io", Vector(1, -4, 3), Vector.origin()),
        Satellite("Europa", Vector(-14, 9, -4), Vector.origin()),
        Satellite("Ganymede", Vector(-4, -6, 7), Vector.origin()),
        Satellite("Callisto", Vector(6, -9, -11), Vector.origin()),
    ]
    part1([m.clone() for m in moons])
    part2([m.clone() for m in moons])


def part1(moons):
    for i in range(0, 1000):
        do_tick(moons)

    total_energy = sum([calculate_energy(moon) for moon in moons])
    print(f"Total Energy: {total_energy}")
    assert 14606 == total_energy


def part2(moons):
    x_period = find_period([m.clone() for m in moons], "x")
    print(f"X Period: {x_period}")

    y_period = find_period([m.clone() for m in moons], "y")
    print(f"Y Period: {y_period}")

    z_period = find_period([m.clone() for m in moons], "z")
    print(f"Z Period: {z_period}")

    total_period = lcm(x_period, y_period, z_period)
    print(f"Total Ticks: {total_period}")
    assert total_period == 543673227860472


if __name__ == "__main__":
    main()
