from intcode import IntCode


def part1(ic: IntCode):
    ic.add_input(1)
    ic.run()
    print(ic.output[0])
    assert ic.output[0] == 5346030


def part2(ic: IntCode):
    ic.add_input(5)
    ic.reset()
    ic.run()
    print(ic.output[0])
    assert ic.output[0] == 513116


if __name__ == "__main__":
    with open("day_05-input.txt", "r") as f:
        ic = IntCode(f.read())
    part1(ic)
    part2(ic)
