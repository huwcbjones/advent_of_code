from unittest import TestCase

from day_23 import State, Amphipod, load_state


class Day23Test(TestCase):
    def test_complete_priority(self):
        state = State(
            [None] * 11,
            [
                [Amphipod.A, Amphipod.A],
                [Amphipod.B, Amphipod.B],
                [Amphipod.C, Amphipod.C],
                [Amphipod.D, Amphipod.D],
            ],
            12521,
        )
        self.assertEqual(0, state.priority)

    def test_in_hallway(self):
        state = State(
            [None, None, None, None, None, None, None, None, None, None, Amphipod.D],
            [
                [Amphipod.A, Amphipod.A],
                [Amphipod.B, Amphipod.B],
                [Amphipod.C, Amphipod.C],
                [Amphipod.D, None],
            ],
            9521,
        )
        self.assertEqual(3000, state.priority)

    def test_is_complete(self):
        state = State(
            [None] * 11,
            [
                [Amphipod.A, Amphipod.A],
                [Amphipod.B, Amphipod.B],
                [Amphipod.C, Amphipod.C],
                [Amphipod.D, Amphipod.D],
            ],
            4519,
        )
        self.assertTrue(state.is_complete)

        state = State(
            [None] * 11,
            [
                [Amphipod.A, Amphipod.A, Amphipod.A, Amphipod.A],
                [Amphipod.B, Amphipod.B, Amphipod.B, Amphipod.B],
                [Amphipod.C, Amphipod.C, Amphipod.C, Amphipod.C],
                [Amphipod.D, Amphipod.D, Amphipod.D, Amphipod.D],
            ],
            0,
        )
        self.assertTrue(state.is_complete)

    def test_is_room_enterable(self):
        state = State(
            [None] * 11,
            [
                [Amphipod.A, None],
                [Amphipod.C, None],
                [None, None],
                [Amphipod.D, Amphipod.D],
            ],
            0,
        )
        self.assertTrue(state.is_room_enterable(0))
        self.assertFalse(state.is_room_enterable(1))
        self.assertTrue(state.is_room_enterable(2))

    def test_is_hallway_clear(self):
        state = State(
            [
                None,
                Amphipod.A,
                None,
                Amphipod.C,
                None,
                None,
                None,
                Amphipod.D,
                None,
                None,
                Amphipod.D,
            ],
            [],
            0,
        )
        self.assertTrue(state.is_hallway_clear(0, 0))
        self.assertTrue(state.is_hallway_clear(1, 2))
        self.assertTrue(state.is_hallway_clear(3, 6))
        self.assertTrue(state.is_hallway_clear(10, 8))

        state = load_state(
            """\
#############
#.B.D.......#
###.#.#C#D###
  #A#B#C#A#  
  #########  """
        )
        self.assertFalse(state.is_hallway_clear(1, 4))
