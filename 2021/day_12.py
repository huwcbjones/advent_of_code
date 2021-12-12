from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from pathlib import Path
from typing import Deque


@dataclass
class Cave:
    name: str
    is_big: bool
    links: set[Cave] = field(default_factory=set)

    def __hash__(self):
        return hash(self.name)

    @classmethod
    def from_name(cls, name: str) -> Cave:
        return cls(name, name.lower() != name)

    def __repr__(self) -> str:
        links = ",".join(c.name for c in self.links)
        return f"<{self.name} -> ({links})>"


def find_unique_paths(caves: dict[str, Cave], small_visits: int = 1) -> set[tuple[str]]:
    paths: set[tuple[str]] = set()
    routes: Deque[tuple[Cave]] = deque()
    routes.append((caves["start"],))
    while routes:
        route = routes.pop()
        for node in route[-1].links:
            if node.name == "end":
                paths.add(tuple(n.name for n in route) + (node.name,))
                continue
            if node.is_big:
                routes.append(route + (node,))
                continue
            if node.name in ("start", "end"):
                continue
            if small_visits == 1:
                if node not in route:
                    routes.append(route + (node,))
                continue

            small_caves = [
                c for c in route if not c.is_big and c.name not in ("start", "end")
            ]
            if len(small_caves) == len(set(small_caves)):
                routes.append(route + (node,))
                continue
            if route.count(node) != 1 and route.count(node) < small_visits:
                routes.append(route + (node,))

    return paths


def main():
    caves: dict[str, Cave] = {}
    with Path(__file__).parent.joinpath("day_12-input.txt").open("r") as input_f:
        for line in input_f.readlines():
            a, b = line.strip().split("-", 1)
            if a not in caves:
                caves[a] = Cave.from_name(a)
            if b not in caves:
                caves[b] = Cave.from_name(b)
            caves[b].links.add(caves[a])
            caves[a].links.add(caves[b])
    print("Part1: ", len(find_unique_paths(caves)))
    print("Part2: ", len(find_unique_paths(caves, 2)))


if __name__ == "__main__":
    main()
