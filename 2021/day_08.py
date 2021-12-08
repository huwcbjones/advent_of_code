from pathlib import Path

DIGIT_MAP: dict[int, set[str]] = {
    2: {"1"},
    3: {"7"},
    4: {"4"},
    7: {"8"},
}


def part1(entries: list[tuple[str, str]]):
    digit_count = 0
    for _digits, output in entries:
        for digit in output:
            unique_segments = len(set(digit))
            if len(DIGIT_MAP.get(unique_segments, set())) == 1:
                digit_count += 1
    return digit_count


def part2(entries: list[tuple[str, str]]):
    numbers: list[int] = []
    for digits, output in entries:
        digit_map = decode_digits(digits)
        digit_map = {"".join(sorted(k)): v for k, v in digit_map.items()}
        numbers.append(int("".join(digit_map["".join(sorted(d))] for d in output)))
    return sum(numbers)


def decode_digits(digits: list[str]) -> dict[str, str]:
    digit_map: dict[str, str] = {}
    inverse_map: dict[str, str] = {}
    top = None
    top_right = None
    bottom_left = None
    middle = None
    while len(inverse_map) < 10:
        # while len(digit_map) != len(digits):
        for digit_code in digits:
            if digit_code in digit_map:
                continue

            segments = set(digit_code)
            if len(segments) == 6 and {"1", "4", "8"} <= set(inverse_map.keys()):
                diff_8 = set(inverse_map["8"]) - segments
                # 9 is a superset of 4
                if (set(inverse_map["4"]) | segments) == segments:
                    digit_map[digit_code] = "9"
                    inverse_map["9"] = digit_code
                    bottom_left = list(diff_8)[0]
                    continue
                # this is a 6
                if diff_8 - set(inverse_map["1"]) == set():
                    digit_map[digit_code] = "6"
                    inverse_map["6"] = digit_code
                    top_right = list(diff_8)[0]
                else:
                    digit_map[digit_code] = "0"
                    inverse_map["0"] = digit_code
                continue

            if len(segments) == 5 and top_right and bottom_left:
                if {top_right, bottom_left} <= segments:
                    digit_map[digit_code] = "2"
                    inverse_map["2"] = digit_code
                elif (segments - {top_right, bottom_left}) == segments:
                    digit_map[digit_code] = "5"
                    inverse_map["5"] = digit_code
                else:
                    digit_map[digit_code] = "3"
                    inverse_map["3"] = digit_code
                continue

            possible_digits = DIGIT_MAP.get(len(set(digit_code)), set())
            for digit in possible_digits:
                if len(possible_digits) == 1:
                    digit_map[digit_code] = digit
                    inverse_map[digit] = digit_code
                    continue
        top = list(set(inverse_map["7"]) - set(inverse_map["1"]))[0]

    if len(inverse_map) != 10:
        raise Exception(digits, inverse_map)
    return digit_map


def main():
    entries = []
    with Path(__file__).parent.joinpath("day_08-input.txt").open("r") as input_f:
        for line in input_f.readlines():
            digits, output = line.split(" | ", 1)
            digits = [d.strip() for d in digits.split(" ")]
            output = [d.strip() for d in output.split(" ")]
            entries.append((digits, output))
    print("Part1: ", part1(entries))
    print("Part2: ", part2(entries))


if __name__ == "__main__":
    main()
