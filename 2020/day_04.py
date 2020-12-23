import re
from typing import Dict, Iterable, List, Tuple
from unittest import TestCase


class Passport(dict, Dict[str, str]):
    REQUIRED_FIELDS = {
        "byr",
        "iyr",
        "eyr",
        "hgt",
        "hcl",
        "ecl",
        "pid",
        "cid",
    }

    _YEAR_REGEX = re.compile(r"\d{4}")
    _COLOUR_REGEX = re.compile(r"#[\da-f]{6}")
    _PID_REGEX = re.compile(r"\d{9}")
    _HGT_REGEX = re.compile(r"(\d+)(cm|in)")

    def is_valid(
        self, extra_validation: bool = False, allow_missing_cid: bool = True
    ) -> bool:
        passport_fields = set(self.keys())
        if allow_missing_cid:
            passport_fields |= {"cid"}

        if self.REQUIRED_FIELDS != passport_fields:
            return False

        if extra_validation:
            for field in passport_fields:
                if validator := getattr(self, f"_validate_{field}", None):
                    if not validator(self[field]):
                        return False
        return True

    @staticmethod
    def _validate_year(value: str, min: int, max: int) -> bool:
        if not Passport._YEAR_REGEX.fullmatch(value):
            return False
        return min <= int(value) <= max

    @staticmethod
    def _validate_byr(value: str) -> bool:
        return Passport._validate_year(value, 1920, 2002)

    @staticmethod
    def _validate_iyr(value: str) -> bool:
        return Passport._validate_year(value, 2010, 2020)

    @staticmethod
    def _validate_eyr(value: str) -> bool:
        return Passport._validate_year(value, 2020, 2030)

    @staticmethod
    def _validate_hcl(value: str) -> bool:
        return bool(Passport._COLOUR_REGEX.fullmatch(value))

    @staticmethod
    def _validate_ecl(value: str) -> bool:
        return value in ("amb", "blu", "brn", "gry", "grn", "hzl", "oth")

    @staticmethod
    def _validate_pid(value: str) -> bool:
        return bool(Passport._PID_REGEX.fullmatch(value))

    @staticmethod
    def _validate_hgt(value: str) -> bool:
        if not (matches := Passport._HGT_REGEX.fullmatch(value)):
            return False
        magnitude = int(matches[1])
        units = matches[2]
        if units == "cm":
            return 150 <= magnitude <= 193
        if units == "in":
            return 59 <= magnitude <= 76
        return False


def parse_batch_file(input: Iterable[str]) -> List[Passport]:
    passports = []
    passport = Passport()
    for line in input:
        if not line or line == "\n":
            passports.append(passport)
            passport = Passport()
            continue
        for entry in line.split(" "):
            key, value = entry.split(":", 1)
            passport[key] = value.strip()
    if passport:
        passports.append(passport)
    return passports


class Day04Test(TestCase):
    batch = (
        "ecl:gry pid:860033327 eyr:2020 hcl:#fffffd",
        "byr:1937 iyr:2017 cid:147 hgt:183cm",
        "",
        "iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884",
        "hcl:#cfa07d byr:1929",
        "",
        "hcl:#ae17e1 iyr:2013",
        "eyr:2024",
        "ecl:brn pid:760753108 byr:1931",
        "hgt:179cm",
        "",
        "hcl:#cfa07d eyr:2025 pid:166559648",
        "iyr:2011 ecl:brn hgt:59in",
    )

    def setUp(self) -> None:
        self.passports = parse_batch_file(self.batch)

    def test_parse_batch(self):
        self.assertListEqual(
            [
                {
                    "ecl": "gry",
                    "pid": "860033327",
                    "eyr": "2020",
                    "hcl": "#fffffd",
                    "byr": "1937",
                    "iyr": "2017",
                    "cid": "147",
                    "hgt": "183cm",
                },
                {
                    "iyr": "2013",
                    "ecl": "amb",
                    "cid": "350",
                    "eyr": "2023",
                    "pid": "028048884",
                    "hcl": "#cfa07d",
                    "byr": "1929",
                },
                {
                    "hcl": "#ae17e1",
                    "iyr": "2013",
                    "eyr": "2024",
                    "ecl": "brn",
                    "pid": "760753108",
                    "byr": "1931",
                    "hgt": "179cm",
                },
                {
                    "hcl": "#cfa07d",
                    "eyr": "2025",
                    "pid": "166559648",
                    "iyr": "2011",
                    "ecl": "brn",
                    "hgt": "59in",
                },
            ],
            self.passports,
        )

    def test_is_passport_valid(self):
        self.assertListEqual(
            [True, False, True, False], [p.is_valid() for p in self.passports]
        )

    def validate_test(self, func, values: List[Tuple[str, bool]]):
        for value, expected in values:
            with self.subTest(value=value):
                self.assertEqual(expected, func(value))

    def test_validate_byr(self):
        self.validate_test(
            Passport._validate_byr,
            [
                ("foo", False),
                ("123", False),
                ("1234", False),
                ("1919", False),
                ("1920", True),
                ("2002", True),
                ("2003", False),
            ],
        )

    def test_validate_iyr(self):
        self.validate_test(
            Passport._validate_iyr,
            [
                ("foo", False),
                ("123", False),
                ("1234", False),
                ("2009", False),
                ("2010", True),
                ("2020", True),
                ("2021", False),
            ],
        )

    def test_validate_eyr(self):
        self.validate_test(
            Passport._validate_eyr,
            [
                ("foo", False),
                ("123", False),
                ("1234", False),
                ("2019", False),
                ("2020", True),
                ("2030", True),
                ("2031", False),
            ],
        )

    def test_vaidate_hgt(self):
        self.validate_test(
            Passport._validate_hgt,
            [("60in", True), ("190cm", True), ("190in", False), ("190", False),],
        )

    def test_invalid_passports(self):
        passports = parse_batch_file(
            """\
eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007
""".splitlines(
                False
            )
        )
        for passport in passports:
            self.assertFalse(passport.is_valid(extra_validation=True))

    def test_valid_passports(self):
        passports = parse_batch_file(
            """\
pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719
""".splitlines(
                False
            )
        )
        for passport in passports:
            self.assertTrue(passport.is_valid(extra_validation=True))


if __name__ == "__main__":
    with open("day_04-input.txt", "r") as fh:
        passports = parse_batch_file(fh)

        part_1 = len([p for p in passports if p.is_valid()])
        print(part_1)  # Part 1: 210

        part_2 = len([p for p in passports if p.is_valid(extra_validation=True)])
        print(part_2)  # Part 2: 131
