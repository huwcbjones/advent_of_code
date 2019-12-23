from dataclasses import dataclass
from functools import lru_cache
from typing import Tuple, Optional, NamedTuple, Union, List


class Vector(NamedTuple):
    x: Union[int, float]
    y: Union[int, float]


class LineSegment(NamedTuple):
    a: Vector
    b: Vector


@lru_cache
def get_line_equation(line: LineSegment) -> Tuple[Optional[float], Optional[float]]:
    m = None
    c = None

    try:
        m = (line.a.y - line.b.y) / (line.a.x - line.b.x)
    except ZeroDivisionError:
        # Line is vertical (x=n)
        return line.a.x, None

    c = line.a.y - m * line.a.x
    return m, c


def get_intersection(a: LineSegment, b: LineSegment) -> Optional[Vector]:
    # Check that the x & y co-ordinates overlap
    if max(a.a.x, a.b.x) < min(b.a.x, b.b.x) or max(a.a.y, a.b.y) < min(b.a.y, b.b.y):
        return None

    # We have two sets of co-ordinates, calculate the line equation for each
    a_m, a_c = get_line_equation(a)
    b_m, b_c = get_line_equation(b)

    # Check if lines are parallel
    if a_m == b_m:
        return None

    # Calculate x co-ord
    if a_c is None:
        # LineA is vertical
        x = a_m
    elif b_c is None:
        # LineB is vertical
        x = b_c
    else:
        x = (b_c - a_c) / (a_m - b_m)

    if a_c is not None:
        y = a_m * x + a_c
    elif b_c is not None:
        y = b_m * x + b_c
    else:
        return None
    return Vector(x, y)


def get_intersections(
    wire_a: List[LineSegment], wire_b: List[LineSegment]
) -> List[Vector]:
    intersections = [get_intersection(a, b) for b in wire_b for a in wire_a]
    return [i for i in intersections if i is not None]


def get_wire(wire_str: str) -> List[LineSegment]:
    lines = []
    x = 0
    y = 0
    start = Vector(x, y)
    for command in wire_str.split(","):

        direction = command[0]
        distance = int(command[1:])
        if direction == "R":
            x += distance
        elif direction == "L":
            x -= distance
        elif direction == "U":
            y += distance
        elif direction == "D":
            y -= distance

        end = Vector(x, y)

        lines.append(LineSegment(start, end))
        start = end

    return lines


if __name__ == "__main__":
    wire_a = get_wire("R8,U5,L5,D3")
    wire_b = get_wire("U7,R6,D4,L4")
    intersections = get_intersections(wire_a, wire_b)
    print(intersections)
