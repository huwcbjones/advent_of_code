def calculate_final_position(
    instructions: list[list[str]], is_complicated: bool = False
) -> int:
    position = depth = aim = 0
    for direction, magnitude in instructions:
        magnitude = int(magnitude)
        if direction == "forward":
            position += magnitude
            if is_complicated:
                depth += aim * magnitude
        if direction == "down":
            if not is_complicated:
                depth += magnitude
            else:
                aim += magnitude
        if direction == "up":
            if not is_complicated:
                depth -= magnitude
            else:
                aim -= magnitude
    return position * depth


def main():
    with open("day_02-input.txt", "r") as input_f:
        instructions: list[list[str]] = [i.split(" ", 1) for i in input_f.readlines()]
    print("Part1: ", calculate_final_position(instructions))
    print("Part2: ", calculate_final_position(instructions, True))


if __name__ == "__main__":
    main()
