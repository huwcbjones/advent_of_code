from intcode import IntCode
import intcode

intcode.SUPPRESS_OUTPUT = False


def part1(ic: IntCode):
    ic.add_input(1)
    ic.run()
    assert ic.output[0] == 3241900951


def part2(ic: IntCode):
    ic.add_input(2)
    ic.reset()
    ic.run()
    assert ic.output[0] == 83089


if __name__ == "__main__":
    with open("day_09-input.txt", "r") as f:
        ic = IntCode(f.read())
    part1(ic)
    part2(ic)
