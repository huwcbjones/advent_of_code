from collections import defaultdict


class IntCode:
    def __init__(self, code: str):
        self._code = code
        self._memory = defaultdict(int)
        self._ip = 0
        self.reset()

    def reset(self):
        self._memory = defaultdict(int)
        instructions = self._code.split(",")
        for i in range(0, len(instructions)):
            self[i] = int(instructions[i])
        self._ip = 0

    def run(self):
        while True:
            instruction = self[self._ip]
            if instruction == 99:
                break

            a = self[self._ip + 1]
            b = self[self._ip + 2]
            r = self[self._ip + 3]

            if instruction == 1:
                self.add(a, b, r)
            elif instruction == 2:
                self.multiply(a, b, r)

            self._ip += 4

    def add(self, a: int, b: int, r: int):
        self[r] = self[a] + self[b]

    def multiply(self, a: int, b: int, r: int):
        self[r] = self[a] * self[b]

    def __getitem__(self, item):
        return self._memory[item]

    def __setitem__(self, key, value):
        self._memory[key] = value