from abc import abstractmethod, ABC
from collections import defaultdict
from dataclasses import dataclass
from enum import IntEnum
from typing import Optional, Dict


class Memory(ABC):
    ip: int

    @abstractmethod
    def __getitem__(self, item: int):
        pass

    @abstractmethod
    def __setitem__(self, key: int, value):
        pass


class HaltException(Exception):
    pass


class ParameterMode(IntEnum):
    POSITION = 0
    IMMEDIATE = 1


@dataclass
class Parameter:
    position: int
    mode: ParameterMode


class Operation(ABC):

    number_of_parameters: Optional[int]
    parameters: Dict[int, Parameter]

    @abstractmethod
    def execute(self, memory: Memory):
        pass

    @staticmethod
    def get_parameter(parameter: Parameter, memory: Memory):
        parameter_pointer = Operation._get_parameter_pointer(parameter, memory)

        if parameter.mode == ParameterMode.IMMEDIATE:
            return memory[parameter_pointer]
        elif parameter.mode == ParameterMode.POSITION:
            return memory[memory[parameter_pointer]]

    @staticmethod
    def set_parameter(parameter: Parameter, memory: Memory, value):
        parameter_pointer = Operation._get_parameter_pointer(parameter, memory)
        memory[memory[parameter_pointer]] = value

    @staticmethod
    def _get_parameter_pointer(parameter: Parameter, memory: Memory):
        return memory.ip + 1 + parameter.position


class Multiply(Operation):
    number_of_parameters = 3

    def execute(self, memory: Memory):
        a = self.get_parameter(self.parameters[0], memory)
        b = self.get_parameter(self.parameters[1], memory)
        self.set_parameter(self.parameters[2], memory, a * b)


class Add(Operation):
    number_of_parameters = 3

    def execute(self, memory: Memory):
        a = self.get_parameter(self.parameters[0], memory)
        b = self.get_parameter(self.parameters[1], memory)
        self.set_parameter(self.parameters[2], memory, a + b)


class Input(Operation):
    number_of_parameters = 1

    def execute(self, memory: Memory):
        value = int(input("<<< "))
        self.set_parameter(self.parameters[0], memory, value)


class Output(Operation):
    number_of_parameters = 1

    def execute(self, memory: Memory):
        value = self.get_parameter(self.parameters[0], memory)
        print(f">>> {value}")


class Halt(Operation):
    number_of_parameters = 0

    def execute(self, memory: Memory):
        raise HaltException()


class JumpIfTrue(Operation):
    number_of_parameters = 2

    def execute(self, memory: Memory):
        value = self.get_parameter(self.parameters[0], memory)
        if value != 0:
            memory.ip = self.get_parameter(self.parameters[1], memory)


class JumpIfFalse(Operation):
    number_of_parameters = 2

    def execute(self, memory: Memory):
        value = self.get_parameter(self.parameters[0], memory)
        if value == 0:
            memory.ip = self.get_parameter(self.parameters[1], memory)


class LessThan(Operation):
    number_of_parameters = 3

    def execute(self, memory: Memory):
        a = self.get_parameter(self.parameters[0], memory)
        b = self.get_parameter(self.parameters[1], memory)
        self.set_parameter(self.parameters[2], memory, int(a < b))


class Equals(Operation):
    number_of_parameters = 3

    def execute(self, memory: Memory):
        a = self.get_parameter(self.parameters[0], memory)
        b = self.get_parameter(self.parameters[1], memory)
        self.set_parameter(self.parameters[2], memory, int(a == b))


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
        99: Halt,
    }

    def __init__(self, code: str):
        self._code = code
        self._memory = defaultdict(int)
        self.ip = 0
        self.reset()

    def reset(self):
        self._memory = defaultdict(int)
        instructions = self._code.split(",")
        for i in range(0, len(instructions)):
            self[i] = int(instructions[i])
        self.ip = 0

    def run(self):
        while True:
            prev_ip = self.ip
            operation = self._parse_opcode(self[self.ip])
            try:
                operation.execute(self)
            except HaltException:
                break

            if self.ip == prev_ip:
                self.ip += operation.number_of_parameters + 1

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
