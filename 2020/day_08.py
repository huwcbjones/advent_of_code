import logging
import re
from abc import ABC, abstractmethod
from typing import Iterable, List
from unittest import TestCase

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger("bootcode")
Argument = int
OP_MAP = {}


def register_op(cls):
    OP_MAP[cls.__name__.lower()] = cls
    return cls


class Computer(ABC):
    ip: int
    accumulator: int


class Operation(ABC):
    def __init__(self, argument: Argument) -> None:
        self.argument = argument

    @abstractmethod
    def execute(self, computer: Computer) -> None:
        pass


class HaltError(Exception):
    def __init__(self, reason: str = None, data=None) -> None:
        super().__init__()
        self.reason = reason
        self.data = data


@register_op
class Acc(Operation):
    def execute(self, computer: Computer) -> None:
        computer.accumulator += self.argument


@register_op
class Jmp(Operation):
    def execute(self, computer: Computer) -> None:
        computer.ip += self.argument


@register_op
class Nop(Operation):
    def execute(self, computer: Computer) -> None:
        pass


class BootCode(Computer):
    INSTRUCTION_REGEX = re.compile(r"([a-z]{3}) ([-+]\d+)")

    def __init__(self, instructions: Iterable[str]):
        self._instructions = list(instructions)
        self.accumulator = 0
        self.ip = 0
        self.halted = False
        self.infinite_loop = False
        self.executed_instructions = set()
        self.reset()

    def reset(self):
        self.accumulator = 0
        self.ip = 0
        self.halted = False
        self.infinite_loop = False
        self.executed_instructions = set()

    @property
    def instructions(self) -> List[str]:
        return self._instructions

    def run(self):
        while not self.halted and self.ip < len(self._instructions):
            if self.ip in self.executed_instructions:
                LOGGER.debug("Infinite Loop Detected!")
                self.infinite_loop = True
                self.halted = True
                break

            prev_ip = self.ip
            operation = self._parse_instruction(self._instructions[self.ip])

            try:
                LOGGER.debug(
                    "Execute OP=%s, IP=%s, AC=%s",
                    type(operation).__name__.lower(),
                    self.ip,
                    self.accumulator,
                )
                operation.execute(self)
            except HaltError as err:
                LOGGER.error("HALTED: %s", err)
                self.halted = True
                break
            finally:
                self.executed_instructions.add(prev_ip)

            if self.ip == prev_ip:
                self.ip += 1

    def _parse_instruction(self, instruction: str) -> Operation:
        if not (matches := self.INSTRUCTION_REGEX.match(instruction)):
            raise HaltError("invalid instruction", instruction)
        op = matches[1]
        argument = int(matches[2])
        if op not in OP_MAP:
            raise HaltError("failed to find operation", {"op": op, "arg": argument})
        return OP_MAP[op](argument)


class BootCodeTest(TestCase):
    def test_execute(self):
        bc = BootCode(
            (
                "nop +0",
                "acc +1",
                "jmp +4",
                "acc +3",
                "jmp -3",
                "acc -99",
                "acc +1",
                "jmp -4",
                "acc +6",
            )
        )
        bc.run()
        self.assertEqual(5, bc.accumulator)


def part2(instructions: List[str]) -> int:
    # brute force swapping one nop/jmp at a time
    for i, instruction in enumerate(instructions):
        if instruction.startswith("nop"):
            old_instruction = instruction
            instructions[i] = instruction.replace("nop", "jmp")
        elif instruction.startswith("jmp"):
            old_instruction = instruction
            instructions[i] = instruction.replace("jmp", "nop")
        else:
            continue

        bc = BootCode(instructions)
        bc.run()
        if bc.infinite_loop:
            # if the program infinite looped, then swap instruction back
            instructions[i] = old_instruction
            continue
        return bc.accumulator


if __name__ == "__main__":
    with open("day_08-input.txt", "r") as fh:
        instructions = fh.read().splitlines(False)
        bc = BootCode(instructions)
        bc.run()
        part_1 = bc.accumulator
        print(part_1)  # Part 1: 1818

        part_2 = part2(instructions)
        print(part_2)  # Part 2: 631
