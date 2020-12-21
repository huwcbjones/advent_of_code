import curses
import time
from collections import defaultdict
from enum import IntEnum
from functools import cached_property
from typing import Tuple, Dict, Optional, Any

from intcode import IntCode


class Tile(IntEnum):
    EMPTY = 0
    WALL = 1
    BLOCK = 2
    PADDLE = 3
    BALL = 4

    @classmethod
    def _missing_(cls, value) -> "Tile":
        """If value is not known, return unknown"""
        return cls.EMPTY


class Joystick(IntEnum):
    LEFT = -1
    NEUTRAL = 0
    RIGHT = 1


class ArcadeCabinet:
    def __init__(self, program: str) -> None:
        self._program = IntCode(program, self._read_joystick_input)
        self._screen_buffer: Dict[Tuple[int, int], Tile] = defaultdict(
            lambda: Tile.EMPTY
        )
        self._score = 0
        self._screen = None

    def reset(self) -> None:
        self._program.reset()

    @staticmethod
    def _init_colours():
        curses.start_color()
        curses.use_default_colors()

        curses.init_pair(Tile.EMPTY, curses.COLOR_BLACK, curses.COLOR_BLACK)
        curses.init_pair(Tile.WALL, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(Tile.BLOCK, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(Tile.PADDLE, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(Tile.BALL, curses.COLOR_RED, curses.COLOR_BLACK)

    @staticmethod
    def _create_window():
        width = 36 + 1
        height = 19 + 2
        return curses.newwin(height, width, 0, 0)

    def run(self) -> None:
        curses.wrapper(self._run)

    def _run(self, stdscr) -> None:
        self._screen = self._create_window()
        self._screen.nodelay(True)
        self._init_colours()

        while not self._program.halted:
            self._program.run(pause_on_output=True)
            x = self._program.output[0]

            self._program.run(pause_on_output=True)
            y = self._program.output[0]

            self._program.run(pause_on_output=True)
            output = self._program.output[0]

            if x == -1 and y == 0:
                self._score = output
                self._screen.addstr(20, 1, f"SCORE: {output}")
            else:
                tile = Tile(output)
                self._screen_buffer[x, y] = tile

                self._screen.addch(
                    y, x, self._get_char_for_tile(tile, x, y), curses.color_pair(tile),
                )
            self._screen.move(20, 36)
            self._screen.refresh()

    @property
    def dimensions(self) -> Tuple[int, int]:
        return 36, 19

    def get_number_of_tiles(self, tile_type: Tile) -> int:
        return len([t for t in self._screen_buffer.values() if t == tile_type])

    def insert_quarter(self, count: int = 1):
        self._program[0] = count

    def _get_char_for_tile(self, tile: Tile, x: int, y: int) -> str:
        width, height = self.dimensions
        if tile is Tile.EMPTY:
            return " "
        if tile is Tile.BLOCK:
            return "◼"
        if tile is Tile.BALL:
            return "●"
        if tile is Tile.PADDLE:
            return "▬"
        if tile is Tile.WALL:
            return self._get_wall_char(x, y, width, height)

    def _get_wall_char(self, x: int, y: int, width: int, height: int) -> str:
        if y == 0:
            if x == 0:
                return "┏"
            if x == width:
                return "┓"
            return "━"
        if y == height:
            if x == 0:
                return "┗"
            if x == width:
                return "┛"
            return "━"
        return "┃"

    def _read_joystick_input(self) -> int:
        delay = 0.4
        start = time.monotonic()
        key = None
        while (taken := time.monotonic() - start) < delay:
            key = self._screen.getch()

            if key in (curses.KEY_LEFT, curses.KEY_RIGHT, ord("r"), ord("a"), ord("d")):
                break
        if key == ord("r"):
            self.reset()

        if taken < delay:
            time.sleep(delay - taken)

        if key == curses.KEY_LEFT or key == ord("a"):
            return Joystick.LEFT
        if key == curses.KEY_RIGHT or key == ord("d"):
            return Joystick.RIGHT
        return Joystick.NEUTRAL


def part1(cabinet: ArcadeCabinet) -> None:
    cabinet.run()
    number_of_blocks = cabinet.get_number_of_tiles(Tile.BLOCK)
    print(number_of_blocks)
    assert number_of_blocks == 270


def part2(cabinet: ArcadeCabinet) -> None:
    cabinet.insert_quarter(2)
    cabinet.run()


def main():
    with open("day_13-input.txt", "r") as f:
        program = f.read()

    cabinet = ArcadeCabinet(program)

    # part1(cabinet)
    # cabinet.reset()

    part2(cabinet)


if __name__ == "__main__":
    main()
