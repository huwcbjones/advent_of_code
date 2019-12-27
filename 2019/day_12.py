from dataclasses import dataclass
from itertools import permutations, product, combinations
from typing import NamedTuple, Tuple, List, Iterable
import time
from math import floor

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


def _apply_gravity(moons: Iterable[Satellite]):
    for a, b in combinations(moons, r=2):
        # print(f"Applying gravity to {a.name[0]}|{b.name[0]}")
        _apply_gravity_to_pair(a, b)


def _apply_gravity_to_pair(a: Satellite, b: Satellite):
    vector = (
        compare(a.position.x, b.position.x),
        compare(a.position.y, b.position.y),
        compare(a.position.z, b.position.z),
    )

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


def do_tick(moons: Iterable[Satellite]):
    _apply_gravity(moons)
    _apply_velocity(moons)


def main():
    moons = [
        Satellite("Io", Vector(1, -4, 3), Vector.origin()),
        Satellite("Europa", Vector(-14, 9, -4), Vector.origin()),
        Satellite("Ganymede", Vector(-4, -6, 7), Vector.origin()),
        Satellite("Callisto", Vector(6, -9, -11), Vector.origin()),
    ]
    # part1(moons)
    part2(moons)


def part1(moons):
    for i in range(0, 1000):
        do_tick(moons)

    total_energy = sum([calculate_energy(moon) for moon in moons])
    print(f"Total Energy: {total_energy}")
    assert 14606 == total_energy


def part2(moons):
    moons = set(moons)
    previous_states = {m.clone() for m in moons}
    counter = 0

    start = time.monotonic()
    while True:
        do_tick(moons)
        counter += 1
        if counter % 1000 == 0:
            time_taken = time.monotonic() - start
            taken = "{:0>2}:{:0>2.0f}".format(floor(time_taken / 60), time_taken % 60)
            print(f"\rProcessed {counter:>10} ticks in {taken}", end="")
        if frozenset(moons) in previous_states:
            break
        previous_states.add(frozenset([m.clone() for m in moons]))

    print(f"Total Ticks: {counter}")
    for moon in moons:
        print(f"{moon}")
    # assert 14606 == total_energy


if __name__ == "__main__":
    main()
