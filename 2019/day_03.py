from functools import lru_cache
from math import sqrt
from typing import Tuple, Optional, NamedTuple, Union, List


class Vector(NamedTuple):
    x: Union[int, float]
    y: Union[int, float]


class LineSegment(NamedTuple):
    a: Vector
    b: Vector


@lru_cache
def get_line_equation(line: LineSegment) -> Tuple[Optional[float], Optional[float]]:
    try:
        m = (line.a.y - line.b.y) / (line.a.x - line.b.x)
    except ZeroDivisionError:
        # Line is vertical (x=n)
        return line.a.x, None

    c = line.a.y - m * line.a.x
    return m, c


@lru_cache
def get_line_length(line: LineSegment) -> Union[float, int]:
    return sqrt((line.a.x - line.b.x) ** 2 + (line.a.y - line.b.y) ** 2)


@lru_cache
def is_point_on_line(point: Vector, line: LineSegment) -> bool:
    m, c = get_line_equation(line)
    if c is None:
        return point.x == m
    return point.y == m * point.x + c


def get_intersection(a: LineSegment, b: LineSegment) -> Optional[Vector]:
    # Check that the x & y co-ordinates overlap
    if (
        max(a.a.x, a.b.x) < min(b.a.x, b.b.x)
        or min(a.a.x, a.b.x) > max(b.a.x, b.b.x)
        or max(a.a.y, a.b.y) < min(b.a.y, b.b.y)
    ):
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
        x = b_m
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


def manhattan_distance(point: Vector) -> Union[int, float]:
    return abs(point.x) + abs(point.y)


def get_path_distance(
    wire: List[LineSegment], intersection: Vector
) -> Union[float, int]:
    distance = 0
    for line in wire:
        if is_point_on_line(intersection, line):
            distance += get_line_length(LineSegment(line.a, intersection))
            break
        distance += get_line_length(line)
    return distance


def part1():
    with open("day_03-input.txt", "r") as f:
        wire_a = get_wire(f.readline())
        wire_b = get_wire(f.readline())

    intersections = get_intersections(wire_a, wire_b)
    print(min([manhattan_distance(p) for p in intersections]))

def part2():
    with open("day_03-input.txt", "r") as f:
        wire_a = get_wire(f.readline())
        wire_b = get_wire(f.readline())

    intersections = get_intersections(wire_a, wire_b)
    distances = {
        i: get_path_distance(wire_a, i) + get_path_distance(wire_b, i)
        for i in intersections
    }
    print("Path: %s" % min(distances.values()))


def process_path(wire_a_str: str, wire_b_str: str):
    wire_a = get_wire(wire_a_str)
    wire_b = get_wire(wire_b_str)
    intersections = get_intersections(wire_a, wire_b)
    print("MHD:  %s" % min([manhattan_distance(p) for p in intersections]))

    distances = {
        i: get_path_distance(wire_a, i) + get_path_distance(wire_b, i)
        for i in intersections
    }
    print("Path: %s" % min(distances.values()))


def test1():
    process_path("R8,U5,L5,D3", "U7,R6,D4,L4")


def test2():
    process_path(
        "R75,D30,R83,U83,L12,D49,R71,U7,L72", "U62,R66,U55,R34,D71,R55,D58,R83"
    )


def test3():
    process_path(
        "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51",
        "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7",
    )


if __name__ == "__main__":
    # test1()
    # test2()
    # test3()
    # part1()
    part2()
