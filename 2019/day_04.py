from typing import Optional, Callable, List


class Combination(int):
    def __init__(self, value: int) -> None:
        super().__init__()
        self._str = [int(i) for i in str(value)]

    def __getitem__(self, item: int):
        return self._str[item]


def is_combination_valid_p1(value: int) -> bool:
    combination = Combination(value)
    prev_value = 0
    has_double_digit = False

    for i in combination:
        # Make sure value is not decreasing
        if i < prev_value:
            return False

        if i == prev_value:
            has_double_digit = True

        prev_value = i
    return has_double_digit


def is_combination_valid_p2(value: int) -> bool:
    combination = Combination(value)
    prev_value: Optional[int] = None
    has_double_digit = False
    repeated_digit_count = 1

    for i in combination:
        # Make sure value is not decreasing
        if prev_value is not None and i < prev_value:
            return False

        if prev_value is None:
            prev_value = i
            continue

        if i == prev_value:
            repeated_digit_count += 1
        else:
            if repeated_digit_count == 2:
                has_double_digit = True
            repeated_digit_count = 1
        prev_value = i
    return repeated_digit_count == 2 or has_double_digit


def get_combinations(start: int, end: int, func: Callable[[int], bool]) -> List[int]:
    return [i for i in range(start, end + 1) if func(i)]


def part1():
    combinations = get_combinations(264793, 803935, is_combination_valid_p1)
    print("P1: %s" % len(combinations))
    assert len(combinations) == 966


def part2():
    combinations = get_combinations(264793, 803935, is_combination_valid_p2)
    print("P2: %s" % len(combinations))
    assert len(combinations) == 628


if __name__ == "__main__":
    part1()
    part2()
