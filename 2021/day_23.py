from __future__ import annotations

import heapq
import logging
from dataclasses import dataclass
from enum import Enum
from functools import cache, total_ordering, cached_property
from pathlib import Path
from typing import Iterator

from profiling import profile


def rindex(lst, value):
    lst.reverse()
    i = lst.index(value)
    lst.reverse()
    return len(lst) - i - 1


class Amphipod(str, Enum):
    A = "A", 0
    B = "B", 1
    C = "C", 2
    D = "D", 3

    def __new__(cls, value, energy_pow):
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj.energy = 10 ** energy_pow
        obj.target_room_idx = energy_pow
        return obj

    def __repr__(self):
        return self.value

    @classmethod
    @cache
    def from_room_idx(cls, room_idx: int) -> Amphipod:
        for i, v in enumerate(cls):
            if i == room_idx:
                return v
        raise KeyError(room_idx)


@total_ordering
@dataclass
class State:
    hallway: list[Amphipod | None]
    rooms: list[list[Amphipod | None]]
    cost: int = 0
    prev_state: State | None = None

    def __repr__(self):
        lines = [
            "#" * (len(self.hallway) + 2),
            "#" + "".join("." if p is None else p for p in self.hallway) + "#",
            "###" + "#".join("." if r[0] is None else r[0] for r in self.rooms) + "###",
        ]
        for i in range(1, len(self.rooms[0])):
            lines.append(
                "  #"
                + "#".join("." if r[i] is None else r[i] for r in self.rooms)
                + "#  "
            )
        lines.append("  " + "#" * (len(self.rooms) * 2 + 1) + "  ")
        return "\n".join(lines)

    def __lt__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.priority < other.priority

    def __hash__(self):
        if not (obj_hash := getattr(self, "_hash", None)):
            hallway = sum(
                i * hash(c)
                for i, c in enumerate(self.hallway, start=1)
                if c is not None
            )
            rooms = sum(
                i * sum(j * hash(pod) for j, pod in enumerate(room, start=1))
                for i, room in enumerate(self.rooms, start=1)
            )
            obj_hash = hallway + rooms + self.cost
            setattr(self, "_hash", obj_hash)
        return obj_hash

    def transitions(self) -> Iterator[State]:
        yield from self._room_to_hallway_transitions()
        yield from self._hallway_to_room_transitions()

    def _iter_empty_spaces(self, start: int) -> Iterator[int]:
        for i in range(start, -1, -1):
            if self.hallway[i] is not None:
                break
            yield i
        for i in range(start + 1, len(self.hallway)):
            if self.hallway[i] is not None:
                break
            yield i

    def _room_to_hallway_transitions(self) -> Iterator[State]:
        for room_idx, room in enumerate(self.rooms):
            if not self.is_room_exitable(room_idx):
                continue

            depth, pod = None, None
            for depth, pod in enumerate(room):
                if pod is not None:
                    break
            if pod is None and depth is None:
                return

            current_pos = self._room_pos(room_idx)

            for target_pos in self._iter_empty_spaces(current_pos):
                if self.is_above_room(target_pos):
                    continue

                steps = depth + 1 + abs(current_pos - target_pos)
                cost = steps * pod.energy

                new_state = self.copy()
                new_state.hallway[target_pos] = pod
                new_state.rooms[room_idx][depth] = None
                new_state.cost += cost
                yield new_state

    def _hallway_to_room_transitions(self) -> Iterator[State]:
        for current_pos, pod in enumerate(self.hallway):
            if pod is None:
                continue
            if not self.is_room_enterable(pod.target_room_idx):
                continue

            target_x = self._room_pos(pod.target_room_idx)
            if not self.is_hallway_clear(current_pos, target_x):
                continue

            target_room_depth = rindex(self.rooms[pod.target_room_idx], None)
            steps = abs(target_x - current_pos) + 1 + target_room_depth
            cost = steps * pod.energy

            new_state = self.copy()
            new_state.hallway[current_pos] = None
            new_state.rooms[pod.target_room_idx][target_room_depth] = pod
            new_state.cost += cost
            yield new_state

    def copy(self) -> State:
        s = State(self.hallway.copy(), [r.copy() for r in self.rooms], self.cost)
        # s.prev_state = self
        return s

    @property
    def is_complete(self) -> bool:
        return all(
            False if i is None else i.target_room_idx == r
            for r, room in enumerate(self.rooms)
            for i in room
        )

    @cached_property
    def priority(self) -> int:
        return (
            self.cost
            + self._cost_exit_room()
            + self._cost_hallway()
            + self._cost_enter_room()
        )

    def _cost_exit_room(self) -> int:
        cost = 0
        for room_idx, room in enumerate(self.rooms):
            current_pos = self._room_pos(room_idx)
            for depth, pod in enumerate(room):
                if pod is None or pod.target_room_idx == room_idx:
                    continue

                hallway_steps = max(
                    abs(current_pos - self._room_pos(pod.target_room_idx)),
                    2,
                )
                steps = depth + 1 + hallway_steps
                cost += steps * pod.energy
        return cost

    def _cost_hallway(self) -> int:
        cost = 0
        for current_pos, pod in enumerate(self.hallway):
            if pod is None:
                continue
            steps = abs(current_pos - self._room_pos(pod.target_room_idx))
            cost += steps * pod.energy
        return cost

    def _cost_enter_room(self) -> int:
        cost = 0
        for room_idx, room in enumerate(self.rooms):
            is_correct = True
            for depth, pod in reversed(list(enumerate(room))):
                if not is_correct:
                    target_pod = Amphipod.from_room_idx(room_idx)
                    steps = depth + 1
                    cost += target_pod.energy * steps
                elif pod is None or pod.target_room_idx != room_idx:
                    is_correct = False
                    continue
        return cost

    @staticmethod
    @cache
    def _room_pos(room_idx: int) -> int:
        return 2 + (room_idx * 2)

    def is_room_enterable(self, room_idx: int) -> bool:
        return all(
            True if pod is None else pod.target_room_idx == room_idx
            for pod in self.rooms[room_idx]
        )

    def is_room_exitable(self, room_idx: int) -> bool:
        return not self.is_room_enterable(room_idx)

    @cache
    def is_above_room(self, pos: int) -> bool:
        return (pos - 2) % 2 == 0 and (pos - 2) / 2 < len(self.rooms)

    def is_hallway_clear(self, start: int, target: int) -> bool:
        if start == target:
            return True
        if start < target:
            start, end = start + 1, target
        else:
            start, end = target, start
        return all(i is None for i in self.hallway[start:end])


def load_state(contents: str) -> State:
    lines = contents.splitlines()
    hallway = [None if c == "." else Amphipod(c) for c in lines[1].replace("#", "")]
    rooms: list[list[Amphipod]] = []
    for line in lines[2:]:
        for i, char in enumerate(line.strip(" #\n").replace("#", "")):
            if len(rooms) < i + 1:
                rooms.insert(i, [])
            pod = None if char == "." else Amphipod(char)
            rooms[i].append(pod)

    return State(hallway, rooms)


@profile(logging.WARNING)
def solve(initial_state: State) -> State:
    stack = [initial_state]
    while stack:
        state = heapq.heappop(stack)
        if state.is_complete:
            return state
        for next_state in state.transitions():
            heapq.heappush(stack, next_state)


def p2_state(initial_state: State) -> State:
    new_pods = {
        1: [Amphipod.D, Amphipod.C, Amphipod.B, Amphipod.A],
        2: [Amphipod.D, Amphipod.B, Amphipod.A, Amphipod.C],
    }
    state = initial_state.copy()
    for insert, pods in new_pods.items():
        for i, pod in enumerate(pods):
            state.rooms[i].insert(insert, Amphipod(pod))
    return state


def print_solution(final_state: State):
    states = [final_state]
    state = final_state
    while state.prev_state is not None:
        states.append(state.prev_state)
        state = state.prev_state
    for i, state in enumerate(list(reversed(states))):
        print(f"{i}: ")
        print(state)


def main():
    with Path(__file__).parent.joinpath("day_23-input.txt").open("r") as input_f:
        initial_state = load_state(input_f.read())

    p1_solution = solve(initial_state)
    print("Part1: ", p1_solution.cost)

    state = p2_state(initial_state)
    p2_solution = solve(state)
    print("Part2: ", p2_solution.cost)


if __name__ == "__main__":
    main()
