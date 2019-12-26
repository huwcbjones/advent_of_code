from abc import abstractmethod, ABC
from collections import defaultdict
from dataclasses import dataclass
from enum import IntEnum
from typing import Optional, Dict, List

SUPPRESS_OUTPUT = True


class ParameterMode(IntEnum):
    POSITION = 0
    IMMEDIATE = 1
    RELATIVE = 2


@dataclass
class Parameter:
    position: int
    mode: ParameterMode


class Memory(ABC):
    ip: int
    relative_base: int

    @abstractmethod
    def __getitem__(self, item: int):
        pass

    @abstractmethod
    def __setitem__(self, key: int, value):
        pass

    @abstractmethod
    def read_input(self):
        pass

    @abstractmethod
    def get(self, address: Parameter):
        pass

    @abstractmethod
    def set(self, address: Parameter, value: int):
        pass


class HaltException(Exception):
    pass


class Operation(ABC):
    number_of_parameters: int
    parameters: Dict[int, Parameter]

    @abstractmethod
    def execute(self, memory: Memory) -> Optional[int]:
        pass


class Multiply(Operation):
    number_of_parameters = 3

    def execute(self, memory: Memory) -> Optional[int]:
        a = memory.get(self.parameters[0])
        b = memory.get(self.parameters[1])
        memory.set(self.parameters[2], a * b)
        return


class Add(Operation):
    number_of_parameters = 3

    def execute(self, memory: Memory) -> Optional[int]:
        a = memory.get(self.parameters[0])
        b = memory.get(self.parameters[1])
        memory.set(self.parameters[2], a + b)
        return


class Input(Operation):
    number_of_parameters = 1

    def execute(self, memory: Memory) -> Optional[int]:
        value = memory.read_input()
        memory.set(self.parameters[0], value)
        return


class Output(Operation):
    number_of_parameters = 1

    def execute(self, memory: Memory) -> Optional[int]:
        value = memory.get(self.parameters[0])
        if not SUPPRESS_OUTPUT:
            print(f">>> {value}\n")
        return value


class Halt(Operation):
    number_of_parameters = 0

    def execute(self, memory: Memory) -> Optional[int]:
        raise HaltException()


class JumpIfTrue(Operation):
    number_of_parameters = 2

    def execute(self, memory: Memory) -> Optional[int]:
        value = memory.get(self.parameters[0])
        if value != 0:
            memory.ip = memory.get(self.parameters[1])
        return


class JumpIfFalse(Operation):
    number_of_parameters = 2

    def execute(self, memory: Memory) -> Optional[int]:
        value = memory.get(self.parameters[0])
        if value == 0:
            memory.ip = memory.get(self.parameters[1])
        return


class LessThan(Operation):
    number_of_parameters = 3

    def execute(self, memory: Memory) -> Optional[int]:
        a = memory.get(self.parameters[0])
        b = memory.get(self.parameters[1])
        memory.set(self.parameters[2], int(a < b))
        return


class Equals(Operation):
    number_of_parameters = 3

    def execute(self, memory: Memory) -> Optional[int]:
        a = memory.get(self.parameters[0])
        b = memory.get(self.parameters[1])
        memory.set(self.parameters[2], int(a == b))
        return


class ChangeRelativeBase(Operation):
    number_of_parameters = 1

    def execute(self, memory: Memory) -> Optional[int]:
        offset = memory.get(self.parameters[0])
        memory.relative_base += offset
        return


class IntCode(Memory):
    op_code_map = {
        1: Add,
        2: Multiply,
        3: Input,
        4: Output,
        5: JumpIfTrue,
        6: JumpIfFalse,
        7: LessThan,
        8: Equals,
        9: ChangeRelativeBase,
        99: Halt,
    }

    def __init__(self, code: str):
        self._code = code
        self._memory = defaultdict(int)
        self.ip = 0
        self.relative_base = 0
        self.output: List[int] = []
        self.input: List[int] = []
        self.halted = False
        self.reset()

    @property
    def code(self) -> str:
        return self._code

    def reset(self):
        self._memory = defaultdict(int)
        instructions = self._code.split(",")
        for i in range(0, len(instructions)):
            self[i] = int(instructions[i])
        self.ip = 0
        self.relative_base = 0
        self.output = []
        self.halted = False

    def run(self, pause_on_output=False):
        while not self.halted:
            prev_ip = self.ip
            operation = self._parse_opcode(self[self.ip])
            try:
                ret_val = operation.execute(self)

            except HaltException:
                self.halted = True
                break

            if self.ip == prev_ip:
                self.ip += operation.number_of_parameters + 1

            if ret_val is None:
                continue

            self.output.insert(0, ret_val)
            if pause_on_output:
                break

    def read_input(self):
        if self.input:
            input_value = self.input.pop(0)
            if not SUPPRESS_OUTPUT:
                print(f"<<< {input_value}")
            return input_value
        else:
            return int(input("<<< "))

    def add_input(self, *values: int):
        self.input += values

    def _parse_opcode(self, op: int) -> Operation:
        instruction_code = f"{op:05}"
        instruction = int(instruction_code[-2:])
        parameters = instruction_code[-3::-1]
        operation = self.op_code_map[instruction]()
        operation.parameters = {
            i: Parameter(i, ParameterMode(int(parameters[i])))
            for i in range(0, operation.number_of_parameters)
        }
        return operation

    def __getitem__(self, item):
        return self._memory[item]

    def __setitem__(self, key, value):
        self._memory[key] = value

    def _get_address(self, address: Parameter):
        if address.mode == ParameterMode.RELATIVE:
            offset = self[self.ip + 1 + address.position]
            return self.relative_base + offset

        address_ptr = self.ip + 1 + address.position
        if address.mode == ParameterMode.POSITION:
            return self[address_ptr]

        return address_ptr

    def get(self, address: Parameter) -> int:
        return self[self._get_address(address)]

    def set(self, address: Parameter, value: int):
        self[self._get_address(address)] = value
