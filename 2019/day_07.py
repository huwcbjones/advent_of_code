from itertools import permutations
from typing import Tuple, List

from intcode import IntCode


def get_thruster_signal(
    ic: IntCode, amplifier_inputs: Tuple[int, int, int, int, int], input_value: int = 0,
):
    amplifiers: List[IntCode] = []
    for i in amplifier_inputs:
        amp = IntCode(ic.code)
        amp.add_input(i)
        amplifiers.append(amp)

    while False in [a.halted for a in amplifiers]:
        for amp in amplifiers:
            amp.add_input(input_value)
            # amp.add_input(amplifier_inputs[i], input_value)
            amp.run(pause_on_output=True)
            input_value = amp.output[0]
    return input_value


def part1():
    with open("day_07-input.txt", "r") as f:
        ic = IntCode(f.read())

    amplifiers = list(range(0, 5))
    results = []
    for config in permutations(amplifiers):
        results.append((config, get_thruster_signal(ic, config)))
    results = sorted(results, key=lambda x: x[1], reverse=True)
    print(results[0])
    assert results[0][1] == 262086


def part2():
    with open("day_07-input.txt", "r") as f:
        ic = IntCode(f.read())

    feedback_amplifiers = list(range(5, 10))
    results = []
    for config in permutations(feedback_amplifiers):
        results.append((config, get_thruster_signal(ic, config)))
    results = sorted(results, key=lambda x: x[1], reverse=True)
    print(results[0])
    assert results[0][1] == 5371621


if __name__ == "__main__":
    part1()
    part2()
