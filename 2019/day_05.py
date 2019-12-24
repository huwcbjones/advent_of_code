from intcode import IntCode


if __name__ == "__main__":
    with open("day_05-input.txt", "r") as f:
        ic = IntCode(f.read())
    ic.run()
