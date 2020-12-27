from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Iterable, Tuple
from unittest import TestCase

from utils import Enum

LOGGER = logging.getLogger("ship")
logging.basicConfig(level=logging.INFO)


class Direction(str, Enum):
    def __new__(cls, value, bearing):
        obj = str.__new__(cls, value)
        obj._value_ = value

        obj.bearing = bearing
        return obj

    NORTH = "N", 0
    EAST = "E", 90
    SOUTH = "S", 180
    WEST = "W", 270

    @classmethod
    def from_bearing(cls, bearing: int) -> Direction:
        assert bearing % 90 == 0
        bearing = bearing % 360
        if bearing == 0:
            return cls.NORTH
        if bearing == 90:
            return cls.EAST
        if bearing == 180:
            return cls.SOUTH
        if bearing == 270:
            return cls.WEST


@dataclass
class Vector:
    x: int
    y: int

    def __eq__(self, o: object) -> bool:
        if isinstance(o, type(self)):
            return self.x == o.x and self.y == o.y
        if isinstance(o, tuple):
            return o == (self.x, self.y)
        return super().__eq__(o)

    def manhattan_distance(self, vector: Vector = None) -> int:
        if vector is None:
            vector = Vector(0, 0)
        return abs(self.x - vector.x) + abs(self.y - vector.y)

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return "{}{}".format(type(self).__name__, str(self))

    def __mul__(self, other):
        if isinstance(other, type(self)):
            x = other.x
            y = other.y
        elif isinstance(other, tuple) and len(other) == 2:
            x, y = other
        elif isinstance(other, int):
            x = other
            y = other
        else:
            raise NotImplemented()
        return Vector(self.x * x, self.y * y)

    def __add__(self, other):
        if isinstance(other, type(self)):
            x = other.x
            y = other.y
        elif isinstance(other, tuple) and len(other) == 2:
            x, y = other
        else:
            raise NotImplemented()
        return Vector(self.x + x, self.y + y)


class Ship:
    def __init__(self):
        self.direction = Direction.EAST
        self.position = Vector(0, 0)

    def process_instruction(self, action: str, value: int):
        if action == "F":
            action = self.direction

        if action in Direction.values():
            if action == Direction.NORTH:
                self.position.y += value
            elif action == Direction.SOUTH:
                self.position.y -= value
            elif action == Direction.EAST:
                self.position.x += value
            elif action == Direction.WEST:
                self.position.x -= value
            LOGGER.info("Move %s %s", action, value)
        elif action in ("L", "R"):
            assert value % 90 == 0
            if action == "L":
                value = 360 - value
            self.direction = Direction.from_bearing(self.direction.bearing + value)
            LOGGER.info("Change direction %s", self.direction)

    @staticmethod
    def parse_instruction(instruction: str) -> Tuple[str, int]:
        action = instruction[0]
        value = int(instruction[1:])
        return action, value

    def run(self, instructions: Iterable[str]):
        for instruction in instructions:
            action, value = self.parse_instruction(instruction)
            self.process_instruction(action, value)

    def __repr__(self) -> str:
        return "{}({}, {})".format(type(self).__name__, self.direction, self.position)


class WaypointShip(Ship):
    def __init__(self):
        super().__init__()
        self.waypoint = Vector(10, 1)

    def process_instruction(self, action: str, value: int):
        if action in Direction.values():
            if action == Direction.NORTH:
                self.waypoint.y += value
            elif action == Direction.SOUTH:
                self.waypoint.y -= value
            elif action == Direction.EAST:
                self.waypoint.x += value
            elif action == Direction.WEST:
                self.waypoint.x -= value
            LOGGER.info("Move waypoint %s %s", action, value)
        elif action in ("L", "R"):
            assert value % 90 == 0
            if action == "L":
                value = 360 - value
            value %= 360
            if value == 90:
                self.waypoint = Vector(self.waypoint.y, -self.waypoint.x)
            elif value == 180:
                self.waypoint = Vector(-self.waypoint.x, -self.waypoint.y)
            elif value == 270:
                self.waypoint = Vector(-self.waypoint.y, self.waypoint.x)
            LOGGER.info("Rotate waypoint %sº", value)
        elif action == "F":
            self.position += self.waypoint * value
            LOGGER.info("Move ship %s x %s", value, self.waypoint)


class ShipTest(TestCase):
    def setUp(self) -> None:
        self.ship = Ship()

    def test_rotate(self):
        self.ship.process_instruction("R", 0)
        self.assertEqual(Direction.EAST, self.ship.direction)
        self.ship.process_instruction("R", 90)
        self.assertEqual(Direction.SOUTH, self.ship.direction)
        self.ship.process_instruction("R", 180)
        self.assertEqual(Direction.NORTH, self.ship.direction)
        self.ship.process_instruction("L", 90)
        self.assertEqual(Direction.WEST, self.ship.direction)
        self.ship.process_instruction("L", 90)
        self.assertEqual(Direction.SOUTH, self.ship.direction)
        self.ship.process_instruction("L", 180)
        self.assertEqual(Direction.NORTH, self.ship.direction)
        self.ship.process_instruction("L", 270)
        self.assertEqual(Direction.EAST, self.ship.direction)

    def test_compass(self):
        with self.subTest(direction="North"):
            self.ship.process_instruction("N", 1)
            self.assertEqual(Direction.EAST, self.ship.direction)
            self.assertEqual(Vector(0, 1), self.ship.position)
        with self.subTest(direction="South"):
            self.ship.process_instruction("S", 1)
            self.assertEqual(Direction.EAST, self.ship.direction)
            self.assertEqual(Vector(0, 0), self.ship.position)
        with self.subTest(direction="East"):
            self.ship.process_instruction("E", 1)
            self.assertEqual(Direction.EAST, self.ship.direction)
            self.assertEqual(Vector(1, 0), self.ship.position)
        with self.subTest(direction="West"):
            self.ship.process_instruction("W", 1)
            self.assertEqual(Direction.EAST, self.ship.direction)
            self.assertEqual(Vector(0, 0), self.ship.position)

    def test_forward(self):
        self.ship.process_instruction("F", 1)
        self.assertEqual(Vector(1, 0), self.ship.position)
        self.ship.process_instruction("F", 10)
        self.assertEqual(Vector(11, 0), self.ship.position)
        self.assertEqual(Direction.EAST, self.ship.direction)

    def test_run(self):
        self.ship.run(["F10", "N3", "F7", "R90", "F11"])
        self.assertEqual(Vector(17, -8), self.ship.position)
        self.assertEqual(Direction.SOUTH, self.ship.direction)
        self.assertEqual(25, self.ship.position.manhattan_distance())


class WaypointShipTest(ShipTest):
    def setUp(self) -> None:
        self.ship = WaypointShip()

    def test_compass(self):
        with self.subTest(direction="North"):
            self.ship.process_instruction("N", 1)
            self.assertEqual(Direction.EAST, self.ship.direction)
            self.assertEqual(Vector(10, 2), self.ship.waypoint)
        with self.subTest(direction="South"):
            self.ship.process_instruction("S", 1)
            self.assertEqual(Direction.EAST, self.ship.direction)
            self.assertEqual(Vector(10, 1), self.ship.waypoint)
        with self.subTest(direction="East"):
            self.ship.process_instruction("E", 1)
            self.assertEqual(Direction.EAST, self.ship.direction)
            self.assertEqual(Vector(11, 1), self.ship.waypoint)
        with self.subTest(direction="West"):
            self.ship.process_instruction("W", 1)
            self.assertEqual(Direction.EAST, self.ship.direction)
            self.assertEqual(Vector(10, 1), self.ship.waypoint)

    def test_rotate(self):
        self.ship.process_instruction("R", 0)
        self.assertEqual(Vector(10, 1), self.ship.waypoint)
        self.ship.process_instruction("R", 90)
        self.assertEqual(Vector(1, -10), self.ship.waypoint)
        self.ship.process_instruction("L", 90)
        self.assertEqual(Vector(10, 1), self.ship.waypoint)
        self.ship.process_instruction("R", 270)
        self.assertEqual(Vector(-1, 10), self.ship.waypoint)
        self.ship.process_instruction("L", 180)
        self.assertEqual(Vector(1, -10), self.ship.waypoint)

    def test_forward(self):
        self.ship.process_instruction("F", 1)
        self.ship.process_instruction("F", 10)
        self.assertEqual(Vector(110, 11), self.ship.position)

    def test_run(self):
        self.ship = WaypointShip()
        instructions = {
            "F10": (Vector(10, 1), Vector(100, 10)),
            "N3": (Vector(10, 4), Vector(100, 10)),
            "F7": (Vector(10, 4), Vector(170, 38)),
            "R90": (Vector(4, -10), Vector(170, 38)),
            "F11": (Vector(4, -10), Vector(214, -72)),
        }
        for instruction, expected in instructions.items():
            with self.subTest(instruction=instruction):
                action, value = self.ship.parse_instruction(instruction)
                self.ship.process_instruction(action, value)
                with self.subTest("waypoint"):
                    self.assertEqual(expected[0], self.ship.waypoint)
                with self.subTest("position"):
                    self.assertEqual(expected[1], self.ship.position)
        self.assertEqual(286, self.ship.position.manhattan_distance())


if __name__ == "__main__":
    with open("day_12-input.txt", "r") as fh:
        instructions = fh.read().splitlines(False)
        ship = Ship()
        ship.run(instructions)

        part_1 = ship.position.manhattan_distance()
        print(part_1)  # Part 1: 796

        ship = WaypointShip()
        ship.run(instructions)
        part_2 = ship.position.manhattan_distance()
        print(part_2)  # Part 2: 39446
