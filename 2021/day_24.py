from __future__ import annotations

import logging
import re
from abc import abstractmethod, ABC
from pathlib import Path
from typing import Iterable, Iterator

LOGGER = logging.getLogger("alu")


class ALU(dict):
    def __getitem__(self, item):
        if isinstance(item, int):
            return item
        return super().__getitem__(item)

    @abstractmethod
    def input(self) -> int:
        pass


OP_MAP = {}


def register_op(cls):
    OP_MAP[cls.__name__.lower()] = cls
    return cls


class Operation(ABC):
    def __init__(self, *arguments: str | int) -> None:
        self.arguments: tuple[str | int, ...] = arguments

    def __getitem__(self, item):
        return self.arguments[item]

    def arg(self, alu: ALU, index: int) -> int:
        value = self[index]
        if isinstance(value, str):
            return alu[value]
        return value

    @abstractmethod
    def execute(self, alu: ALU) -> None:
        pass

    def __repr__(self):
        args = " ".join(str(a) for a in self.arguments)
        return f"{type(self).__name__.lower()} {args}"


@register_op
class Inp(Operation):
    def execute(self, alu: ALU) -> None:
        alu[self[0]] = alu.input()


@register_op
class Add(Operation):
    def execute(self, alu: ALU) -> None:
        alu[self[0]] += self.arg(alu, 1)


@register_op
class Mul(Operation):
    def execute(self, alu: ALU) -> None:
        alu[self[0]] *= self.arg(alu, 1)


@register_op
class Div(Operation):
    def execute(self, alu: ALU) -> None:
        alu[self[0]] //= self.arg(alu, 1)


@register_op
class Mod(Operation):
    def execute(self, alu: ALU) -> None:
        alu[self[0]] %= self.arg(alu, 1)


@register_op
class Eql(Operation):
    def execute(self, alu: ALU) -> None:
        alu[self[0]] = int(self.arg(alu, 0) == self.arg(alu, 1))


class ALUProgram(ALU):
    INSTRUCTION_REGEX = re.compile(
        r"(?P<OP>[a-z]{3}) (?P<A>[wxyz]|-?\d+)(?: (?P<B>[wxyz]|-?\d+))?"
    )

    def __init__(self, instructions: Iterable[str], inputs: list[int] = None):
        super().__init__()
        self._instructions = list(instructions)
        self._inputs = inputs or []
        self._inp_p = 0
        self.ip = 0
        self.halted = False
        self.reset()

    def reset(self):
        self.clear()
        self.update({"w": 0, "x": 0, "y": 0, "z": 0})
        self.ip = 0
        self._inp_p = 0
        self.halted = False

    @property
    def instructions(self) -> list[str]:
        return self._instructions

    def input(self) -> int:
        if self._inp_p < len(self._inputs):
            try:
                return self._inputs[self._inp_p]
            finally:
                self._inp_p += 1
        return int(input("Enter value: "))

    def run(self):
        while not self.halted and self.ip < len(self.instructions):
            operation = self._parse_instruction(self.instructions[self.ip])
            LOGGER.debug(
                "Execute OP=%s, IP=%s, Args=%s, State=%s",
                type(operation).__name__.lower(),
                self.ip,
                operation.arguments,
                self,
            )
            operation.execute(self)
            self.ip += 1
        self.halted = True

    def _parse_instruction(self, instruction: str) -> Operation:
        if not (matches := self.INSTRUCTION_REGEX.match(instruction)):
            raise RuntimeError("invalid instruction", instruction)
        op = matches["OP"]
        args = []
        for arg in ["A", "B"]:
            if value := matches[arg]:
                try:
                    value = int(value)
                except ValueError:
                    pass
                args.append(value)

        if op not in OP_MAP:
            raise RuntimeError("failed to find operation", {"op": op, "args": args})
        return OP_MAP[op](*args)


class ModelValidatingALUProgram(ALUProgram):
    def __init__(self, instructions: Iterable[str], model_number: int = 0):
        super().__init__(instructions)
        self.model_number = model_number
        self.set_model_number(model_number)

    def set_model_number(self, number: int):
        self.model_number = number
        self._inputs = [int(i) for i in f"{number:0>14}"]


def part1(program: ModelValidatingALUProgram) -> int | None:
    program.reset()
    program.run()
    if program["z"] == 0:
        return program.model_number
    return None


def main():
    with Path(__file__).parent.joinpath("day_24-input.txt").open("r") as input_f:
        program = ModelValidatingALUProgram(input_f.readlines())
    program.set_model_number(96299896449997)
    print("Part1: ", part1(program))

    program.reset()
    program.set_model_number(31162141116841)
    print("Part1: ", part1(program))


if __name__ == "__main__":
    main()
