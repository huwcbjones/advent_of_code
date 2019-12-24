from StringIO import StringIO
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


def part1():
    with open("day_06-input.txt", "r") as f:
        objects = parse_map(f)

    print(sum([o.orbit_count for o in objects.values() if o.id != "COM"]))


def part2():
    objects = parse_map(
        StringIO(
            "COM)B\nB)C\nC)D\nD)E\nE)F\nB)G\nG)H\nD)I\nE)J\nJ)K\nK)L\nK)YOU\nI)SAN"
        )
    )


if __name__ == "__main__":
    part1()
    # part2()
