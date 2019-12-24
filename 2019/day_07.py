from itertools import permutations
from typing import Tuple
from unittest import mock

from intcode import IntCode


@mock.patch("intcode.input")
def get_thruster_signal(
    ic: IntCode,
    amplifiers: Tuple[int, int, int, int, int],
    mock_input,
    input_value: int = 0,
):

    for i in amplifiers:
        ic.reset()
        mock_input.side_effect = [i, input_value]
        ic.run()
        input_value = ic.output[0]
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


def part2():
    with open("day_07-input.txt", "r") as f:
        ic = IntCode(f.read())

    amplifiers = list(range(0, 5))
    feedback_amplifiers = list(range(5, 10))
    results = []
    for amp in permutations(amplifiers):
        phase_1 = get_thruster_signal(ic, amp)
        for feedback in permutations(feedback_amplifiers):
            phase_2 = get_thruster_signal(ic, feedback, input_value=phase_1)
            results.append((amp + feedback, get_thruster_signal(ic, amp)))
    results = sorted(results, key=lambda x: x[1], reverse=True)
    print(results[0])


if __name__ == "__main__":
    # part1()
    part2()
