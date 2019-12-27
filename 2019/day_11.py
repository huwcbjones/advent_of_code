from collections import defaultdict
from enum import IntEnum
from typing import Tuple, Dict

from intcode import IntCode


class Direction(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


class NumberPlate:
    def __init__(self):
        self._plate: Dict[Tuple[int, int], int] = defaultdict(int)

    def __getitem__(self, item: Tuple[int, int]):
        return self._plate[item]

    def __setitem__(self, key: Tuple[int, int], value: int):
        self._plate[key] = value

    def get_plate(self) -> str:
        x_cords = [p[0] for p in self._plate.keys()]
        y_cords = [p[1] for p in self._plate.keys()]
        min_x = min(x_cords)
        max_x = max(x_cords)
        min_y = min(y_cords)
        max_y = max(y_cords)
        return "\n".join(
            [
                "".join([str(self[x, y]) for x in range(min_x, max_x + 1)])
                for y in range(min_y, max_y + 1)
            ]
        )


class Robot:
    move_map = {
        Direction.UP: (0, -1),
        Direction.RIGHT: (1, 0),
        Direction.DOWN: (0, 1),
        Direction.LEFT: (-1, 0),
    }

    def __init__(self, brain: IntCode) -> None:
        self._brain = brain
        self._brain.reset()
        self._direction = Direction.UP
        self._x = 0
        self._y = 0

    def set_position(self, x: int, y: int) -> None:
        self._x = x
        self._y = y

    def _move(self) -> None:
        movement = self.move_map[self._direction]
        self._x += movement[0]
        self._y += movement[1]

    def _turn(self, direction: int) -> None:
        if direction == 0:
            new_direction = (self._direction + 3) % 4
        else:
            new_direction = (self._direction + 1) % 4
        self._direction = Direction(new_direction)

    def paint(self, plate: NumberPlate) -> None:
        while not self._brain.halted:
            self._brain.add_input(plate[self._x, self._y])

            self._brain.run(pause_on_output=True)
            plate[self._x, self._y] = self._brain.output[0]

            self._brain.run(pause_on_output=True)
            self._turn(direction=self._brain.output[0])
            self._move()


def part1(brain: IntCode):
    plate = NumberPlate()
    plate[0, 0] = 1
    robot = Robot(brain)
    robot.paint(plate)
    licence_plate = plate.get_plate()
    print(licence_plate.replace("1", "█").replace("0", "░"))


def main():
    with open("day_11-input.txt", "r") as f:
        brain = IntCode(f.read())
    part1(brain)


if __name__ == "__main__":
    main()
