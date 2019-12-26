from dataclasses import dataclass
from typing import IO, Optional, Set, Dict


@dataclass
class Object:
    id: str
    parent: Optional["Object"]
    children: Set["Object"]
    orbit_count: Optional[int] = None

    def __hash__(self) -> int:
        return self.id.__hash__()

    def __repr__(self) -> str:
        return f"Object({self.id}: {len(self.children)})"


def parse_map(map_file: IO) -> Dict[str, Object]:
    objects = {"COM": Object("COM", None, set(), 0)}
    for line in map_file.readlines():
        parent_id, child_id = line.strip().split(")", 1)

        if parent_id not in objects:
            parent = Object(parent_id, None, set())
            objects[parent.id] = parent
        else:
            parent = objects[parent_id]
        if child_id in objects:
            child = objects[child_id]
        else:
            child = Object(child_id, parent, set())
        child.parent = parent
        if parent.orbit_count is not None:
            child.orbit_count = parent.orbit_count + 1
        parent.children.add(child)
        objects[child.id] = child

    calculate_object_orbits(objects["COM"])

    return objects


def calculate_object_orbits(obj: Object):
    for child in obj.children:
        if child.orbit_count is None:
            child.orbit_count = obj.orbit_count + 1
        calculate_object_orbits(child)


def get_route_to_com(obj: Object):
    route = []
    while obj := obj.parent:
        route.append(obj.id)
    route.reverse()
    return route


def get_route_between_nodes(start: Object, end: Object):
    start_to_com = get_route_to_com(start)
    end_to_com = get_route_to_com(end)
    i, j = 0, 0
    intersection = None

    while i != len(start_to_com) or j != len(end_to_com):

        # Keep moving forward until no intersection is found
        if i == j and start_to_com[i] == end_to_com[j]:
            i += 1
            j += 1
        else:
            intersection = j - 1
            break
    return (
        start_to_com[len(start_to_com) : intersection : -1]
        + end_to_com[intersection : len(end_to_com)]
    )


def part1():
    with open("day_06-input.txt", "r") as f:
        objects = parse_map(f)
    orbit_count = sum([o.orbit_count for o in objects.values() if o.id != "COM"])
    print(orbit_count)
    assert orbit_count == 417916


def part2():
    with open("day_06-input.txt", "r") as f:
        objects = parse_map(f)
    route = get_route_between_nodes(objects["YOU"], objects["SAN"])
    orbital_hops = len(route) - 1
    print(orbital_hops)
    assert orbital_hops == 523


if __name__ == "__main__":
    part1()
    part2()
