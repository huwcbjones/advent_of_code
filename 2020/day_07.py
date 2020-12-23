import re
from collections import defaultdict
from typing import Dict, Iterable, List, Set
from unittest import TestCase

RULE_REGEX = re.compile(r"([a-z ]+) bags contain (.*)\.")
BAG_REGEX = re.compile(r"(\d+) ([a-z ]+) bags?")


def parse_rules(input: Iterable[str]) -> Dict[str, Dict[str, int]]:
    rules = {}
    for rule in input:
        if not (matches := RULE_REGEX.match(rule)):
            continue
        colour = matches[1]
        bag_rules = {}
        bags = matches[2].split(", ")
        for bag in bags:
            if not (matches := BAG_REGEX.match(bag)):
                continue
            bag_rules[matches[2]] = int(matches[1])
        rules[colour] = bag_rules
    return rules


def create_inverse_map(rules: Dict[str, Dict[str, int]]) -> Dict[str, Set[str]]:
    bag_map = defaultdict(set)
    for inner_bag, bag_rules in rules.items():
        for outer_bag in bag_rules.keys():
            bag_map[outer_bag].add(inner_bag)
    return bag_map


def calculate_maximum_containers(rules: Dict[str, Dict[str, int]], target: str) -> int:
    bag_map = create_inverse_map(rules)
    container_bags = set()
    targets = [target]
    while targets:
        target = targets.pop()
        new_containers = bag_map[target]
        container_bags |= new_containers
        targets.extend(new_containers)
    return len(container_bags)


def calculate_total_bag_count(rules: Dict[str, Dict[str, int]], target: str) -> int:
    return sum(rules[target].values()) + sum(
        c * calculate_total_bag_count(rules, b) for b, c in rules[target].items()
    )


class Day07Test(TestCase):
    def setUp(self) -> None:
        self.rules = parse_rules(
            (
                "light red bags contain 1 bright white bag, 2 muted yellow bags.",
                "dark orange bags contain 3 bright white bags, 4 muted yellow bags.",
                "bright white bags contain 1 shiny gold bag.",
                "muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.",
                "shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.",
                "dark olive bags contain 3 faded blue bags, 4 dotted black bags.",
                "vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.",
                "faded blue bags contain no other bags.",
                "dotted black bags contain no other bags.",
            )
        )

    def test_parse_rules(self):
        expected = {
            "light red": {"bright white": 1, "muted yellow": 2,},
            "dark orange": {"bright white": 3, "muted yellow": 4,},
            "bright white": {"shiny gold": 1,},
            "muted yellow": {"shiny gold": 2, "faded blue": 9,},
            "shiny gold": {"dark olive": 1, "vibrant plum": 2,},
            "dark olive": {"faded blue": 3, "dotted black": 4},
            "vibrant plum": {"faded blue": 5, "dotted black": 6,},
            "faded blue": {},
            "dotted black": {},
        }
        for key, value in self.rules.items():
            with self.subTest(key=key):
                self.assertIn(key, expected)
                self.assertDictEqual(expected[key], value)

    def test_create_bag_map(self):
        expected = {
            "bright white": {"light red", "dark orange"},
            "muted yellow": {"light red", "dark orange"},
            "shiny gold": {"bright white", "muted yellow"},
            "faded blue": {"muted yellow", "dark olive", "vibrant plum"},
            "dark olive": {"shiny gold"},
            "vibrant plum": {"shiny gold"},
            "dotted black": {"dark olive", "vibrant plum"},
        }
        bag_map = create_inverse_map(self.rules)
        for key, value in bag_map.items():
            with self.subTest(key=key):
                self.assertIn(key, expected)
                self.assertSetEqual(expected[key], value)

    def test_calculate_container_count(self):
        self.assertEqual(4, calculate_maximum_containers(self.rules, "shiny gold"))

    def test_calculate_total_bag_count(self):
        self.assertEqual(32, calculate_total_bag_count(self.rules, "shiny gold"))

        rules = parse_rules(
            (
                "shiny gold bags contain 2 dark red bags.",
                "dark red bags contain 2 dark orange bags.",
                "dark orange bags contain 2 dark yellow bags.",
                "dark yellow bags contain 2 dark green bags.",
                "dark green bags contain 2 dark blue bags.",
                "dark blue bags contain 2 dark violet bags.",
                "dark violet bags contain no other bags.",
            )
        )
        self.assertEqual(126, calculate_total_bag_count(rules, "shiny gold"))


if __name__ == "__main__":
    with open("day_07-input.txt", "r") as fh:
        rules = parse_rules(fh)

        part_1 = calculate_maximum_containers(rules, "shiny gold")
        print(part_1)  # Part 1: 211

        part_2 = calculate_total_bag_count(rules, "shiny gold")
        print(part_2)  # Part 2: 12414
