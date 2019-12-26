from intcode import IntCode


def part1(ic: IntCode):
    ic[1] = 12
    ic[2] = 2
    ic.run()
    assert ic[0] == 3058646
    print(ic[0])


def part2(ic: IntCode):
    for i in range(0, 100):
        for j in range(0, 100):
            ic.reset()
            ic[1] = i
            ic[2] = j
            ic.run()
            if ic[0] == 19690720:
                print(f"{i}, {j} = {ic[0]}")
                assert i == 89 and j == 76
                break


if __name__ == "__main__":
    with open("day_02-input.txt", "r") as f:
        ic = IntCode(f.read())
    part1(ic)
    part2(ic)
