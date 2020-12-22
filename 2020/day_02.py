import re
from dataclasses import dataclass
from typing import Tuple
from unittest import TestCase


@dataclass
class Policy:
    min: int
    max: int
    char: str

    @property
    def pos_a(self) -> int:
        return self.min

    @property
    def pos_b(self) -> int:
        return self.max


PASSWORD_ENTRY_REGEX = re.compile(r"(\d+)-(\d+) ([a-z]+): (.*)")


def parse_password_entry(data: str) -> Tuple[str, Policy]:
    matches = PASSWORD_ENTRY_REGEX.match(data)
    assert matches
    return matches[4], Policy(int(matches[1]), int(matches[2]), matches[3])


def validate_sled_password(password: str, policy: Policy) -> bool:
    return policy.min <= password.count(policy.char) <= policy.max


def validate_sled_password_entry(entry: str) -> bool:
    password, policy = parse_password_entry(entry)
    return validate_sled_password(password, policy)


def validate_toboggan_password(password: str, policy: Policy) -> bool:
    return (password[policy.pos_a - 1] == policy.char) ^ (
        password[policy.pos_b - 1] == policy.char
    )


def validate_toboggan_password_entry(entry: str) -> bool:
    password, policy = parse_password_entry(entry)
    return validate_toboggan_password(password, policy)


class Day2Test(TestCase):
    def test_parse_entry(self):
        self.assertTupleEqual(
            ("abcde", Policy(1, 3, "a")), parse_password_entry("1-3 a: abcde")
        )
        self.assertTupleEqual(
            ("cdefg", Policy(1, 3, "b")), parse_password_entry("1-3 b: cdefg")
        )
        self.assertTupleEqual(
            ("ccccccccc", Policy(2, 9, "c")), parse_password_entry("2-9 c: ccccccccc")
        )

    def test_validate_sled_password(self):
        self.assertTrue(validate_sled_password_entry("1-3 a: abcde"))
        self.assertFalse(validate_sled_password_entry("1-3 b: cdefg"))
        self.assertTrue(validate_sled_password_entry("1-9 c: ccccccccc"))

    def test_validate_toboggan_password(self):
        self.assertTrue(validate_toboggan_password_entry("1-3 a: abcde"))
        self.assertFalse(validate_toboggan_password_entry("1-3 b: cdefg"))
        self.assertFalse(validate_toboggan_password_entry("2-9 c: ccccccccc"))


if __name__ == "__main__":
    with open("day_02-input.txt", "r") as fh:
        part_1 = len([l for l in fh if validate_sled_password_entry(l)])
        print(part_1)  # Part 1: 614

        fh.seek(0)

        part_2 = len([l for l in fh if validate_toboggan_password_entry(l)])
        print(part_2)  # Part 2: 354
