from math import log10
from unittest import TestCase

import intcode
from intcode import IntCode


class IntCodeTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        intcode.SUPPRESS_OUTPUT = False

    def test_add(self):
        ic = IntCode("1, 1, 2, 0, 99")
        ic.run()
        self.assertEqual(3, ic[0])

    def test_multiply(self):
        ic = IntCode("2, 1, 2, 0, 99")
        ic.run()
        self.assertEqual(2, ic[0])

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

    def test_relative_mode_output(self):
        ic = IntCode("109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99")
        ic.run()
        output = reversed(ic.output)
        output_code = ",".join([str(i) for i in output])
        self.assertEqual(ic._code, output_code)

    def test_relative_mode_16_digit_number(self):
        ic = IntCode("1102,34915192,34915192,7,4,7,99,0")
        ic.run()
        self.assertEqual(16, int(log10(ic.output[0])) + 1)

    def test_relative_mode(self):
        ic = IntCode("104,1125899906842624,99")
        ic.run()
        self.assertEqual(1125899906842624, ic.output[0])
