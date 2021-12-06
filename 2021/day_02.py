def part1(instructions):
    position = 0
    depth = 0
    for direction, magnitude in instructions:
        magnitude = int(magnitude)
        if direction == "forward":
            position += magnitude
        if direction == "down":
            depth += magnitude
        if direction == "up":
            depth -= magnitude
    print(position, depth)
    print(position * depth)


def part2(instructions):
    position = 0
    depth = 0
    aim = 0
    for direction, magnitude in instructions:
        magnitude = int(magnitude)
        if direction == "forward":
            position += magnitude
            depth += aim * magnitude
        if direction == "down":
            aim += magnitude
        if direction == "up":
            aim -= magnitude
    print(position, depth)
    print(position * depth)


if __name__ == "__main__":
    with open("day_02-input.txt", "r") as input_f:
        instructions = [i.split(" ", 1) for i in input_f.readlines()]
    part1(instructions)
    part2(instructions)
