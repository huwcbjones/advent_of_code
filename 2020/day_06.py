from typing import Iterable, List, Sequence, Set
from unittest import TestCase


def parse_groups(people: Iterable[str]) -> List[List[str]]:
    groups = []
    group = []
    for person in people:
        if not person.strip():
            groups.append(group)
            group = []
            continue
        group.append(person.strip())
    if group:
        groups.append(group)
    return groups


def get_answerable_questions(group: Sequence[str], everyone: bool) -> Set[str]:
    questions = set()
    if not group:
        return questions

    if everyone:
        # need to initialise starting set, else nothing will be added
        questions = set(group[0])

    for person in group:
        if everyone:
            questions &= set(person)
        else:
            questions |= set(person)
    return questions


def get_question_count(group: Sequence[str], everyone: bool) -> int:
    return len(get_answerable_questions(group, everyone))


class Day06Test(TestCase):
    def setUp(self) -> None:
        self.groups = parse_groups(
            ["abc", "", "a", "b", "c", "", "ab", "ac", "", "a", "a", "a", "a", "", "b"]
        )

    def test_get_answerable_questions_someone(self):
        self.assertSetEqual({"a", "b", "c"}, get_answerable_questions(["abc"], False))
        self.assertSetEqual(
            {"a", "b", "c"}, get_answerable_questions(["a", "b", "c"], False)
        )
        self.assertSetEqual(
            {"a", "b", "c"}, get_answerable_questions(["ab", "ac"], False)
        )
        self.assertSetEqual(
            {"a"}, get_answerable_questions(["a", "a", "a", "a"], False)
        )
        self.assertSetEqual({"b"}, get_answerable_questions(["b"], False))

    def test_get_answerable_questions_everyone(self):
        self.assertSetEqual({"a", "b", "c"}, get_answerable_questions(["abc"], True))
        self.assertSetEqual(set(), get_answerable_questions(["a", "b", "c"], True))
        self.assertSetEqual({"a"}, get_answerable_questions(["ab", "ac"], True))
        self.assertSetEqual({"a"}, get_answerable_questions(["a", "a", "a", "a"], True))
        self.assertSetEqual({"b"}, get_answerable_questions(["b"], True))

    def test_get_question_count(self):
        self.assertEqual(3, get_question_count(["abc"], False))
        self.assertEqual(3, get_question_count(["a", "b", "c"], False))
        self.assertEqual(3, get_question_count(["ab", "ac"], False))
        self.assertEqual(1, get_question_count(["a", "a", "a", "a"], False))
        self.assertEqual(1, get_question_count(["b"], False))

    def test_get_question_count_everyone(self):
        self.assertEqual(3, get_question_count(["abc"], True))
        self.assertEqual(0, get_question_count(["a", "b", "c"], True))
        self.assertEqual(1, get_question_count(["ab", "ac"], True))
        self.assertEqual(1, get_question_count(["a", "a", "a", "a"], True))
        self.assertEqual(1, get_question_count(["b"], True))

    def test_parse_groups(self):
        self.assertListEqual(
            [["abc"], ["a", "b", "c"], ["ab", "ac"], ["a", "a", "a", "a"], ["b"]],
            self.groups,
        )


if __name__ == "__main__":
    with open("day_06-input.txt", "r") as fh:
        groups = parse_groups(fh)

        part_1 = sum([get_question_count(g, False) for g in groups])
        print(part_1)  # Part 1: 6551

        part_2 = sum([get_question_count(g, True) for g in groups])
        print(part_2)  # Part 2: 3358
