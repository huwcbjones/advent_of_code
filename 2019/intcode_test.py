from unittest import TestCase, mock

from intcode import IntCode


class IntCodeTest(TestCase):
    def test_simple(self):
        ic = IntCode("1,9,10,3,2,3,11,0,99,30,40,50")
        ic.run()
        self.assertEqual(
            [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50], list(ic._memory.values())
        )

    def test_inputoutput(self):
        ic = IntCode("3,0,4,0,99")
        ic.add_input(8)
        ic.run()
        self.assertEqual(8, ic.output[0])

    def test_equal_to_8_position(self):
        ic = IntCode("3,9,8,9,10,9,4,9,99,-1,8")
        ic.add_input(8)
        ic.run()
        self.assertEqual(1, ic.output[0])

        ic.reset()
        ic.add_input(7)
        ic.run()
        self.assertEqual(0, ic.output[0])

    def test_less_than_8_position(self):
        ic = IntCode("3,9,7,9,10,9,4,9,99,-1,8")
        ic.add_input(7)
        ic.run()
        self.assertEqual(1, ic.output[0])

        ic.add_input(8)
        ic.reset()
        ic.run()
        self.assertEqual(0, ic.output[0])

    def test_equal_to_8_immediate(self):
        ic = IntCode("3,3,1108,-1,8,3,4,3,99")
        ic.add_input(8)
        ic.run()
        self.assertEqual(1, ic.output[0])

        ic.add_input(7)
        ic.reset()
        ic.run()
        self.assertEqual(0, ic.output[0])

    def test_less_than_8_immediate(self):
        ic = IntCode("3,3,1107,-1,8,3,4,3,99")
        ic.add_input(7)
        ic.run()
        self.assertEqual(1, ic.output[0])

        ic.add_input(8)
        ic.reset()
        ic.run()
        self.assertEqual(0, ic.output[0])

    def test_jump_position(self):
        ic = IntCode("3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9")
        ic.add_input(0)
        ic.run()
        self.assertEqual(0, ic.output[0])

        ic.add_input(1)
        ic.reset()
        ic.run()
        self.assertEqual(1, ic.output[0])

    def test_jump_immediate(self):
        ic = IntCode("3,3,1105,-1,9,1101,0,0,12,4,12,99,1")
        ic.add_input(0)
        ic.run()
        self.assertEqual(0, ic.output[0])

        ic.add_input(1)
        ic.reset()
        ic.run()
        self.assertEqual(1, ic.output[0])

    def test_equality(self):
        ic = IntCode(
            """
3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99"""
        )
        ic.add_input(7)
        ic.run()
        self.assertEqual(999, ic.output[0])

        ic.add_input(8)
        ic.reset()
        ic.run()
        self.assertEqual(1000, ic.output[0])

        ic.add_input(9)
        ic.reset()
        ic.run()
        self.assertEqual(1001, ic.output[0])
