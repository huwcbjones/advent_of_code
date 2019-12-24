from unittest import TestCase, mock

from intcode import IntCode


class IntCodeTest(TestCase):
    def test_simple(self):
        ic = IntCode("1,9,10,3,2,3,11,0,99,30,40,50")
        ic.run()
        self.assertEqual(
            [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50], list(ic._memory.values())
        )

    @mock.patch("intcode.print")
    @mock.patch("intcode.input")
    def test_inputoutput(self, mock_input, mock_print):
        mock_input.return_value = 8
        ic = IntCode("3,0,4,0,99")
        ic.run()
        self.assertIn("8", mock_print.call_args[0][0])

    @mock.patch("intcode.print")
    @mock.patch("intcode.input")
    def test_equal_to_8_position(self, mock_input, mock_print):
        ic = IntCode("3,9,8,9,10,9,4,9,99,-1,8")
        mock_input.return_value = 8
        ic.run()
        self.assertIn("1", mock_print.call_args[0][0])

        mock_input.return_value = 7
        ic.reset()
        ic.run()
        self.assertIn("0", mock_print.call_args[0][0])

    @mock.patch("intcode.print")
    @mock.patch("intcode.input")
    def test_less_than_8_position(self, mock_input, mock_print):
        ic = IntCode("3,9,7,9,10,9,4,9,99,-1,8")
        mock_input.return_value = 7
        ic.run()
        self.assertIn("1", mock_print.call_args[0][0])

        mock_input.return_value = 8
        ic.reset()
        ic.run()
        self.assertIn("0", mock_print.call_args[0][0])

    @mock.patch("intcode.print")
    @mock.patch("intcode.input")
    def test_equal_to_8_immediate(self, mock_input, mock_print):
        ic = IntCode("3,3,1108,-1,8,3,4,3,99")
        mock_input.return_value = 8
        ic.run()
        self.assertIn("1", mock_print.call_args[0][0])

        mock_input.return_value = 7
        ic.reset()
        ic.run()
        self.assertIn("0", mock_print.call_args[0][0])

    @mock.patch("intcode.print")
    @mock.patch("intcode.input")
    def test_less_than_8_immediate(self, mock_input, mock_print):
        ic = IntCode("3,3,1107,-1,8,3,4,3,99")
        mock_input.return_value = 7
        ic.run()
        self.assertIn("1", mock_print.call_args[0][0])

        mock_input.return_value = 8
        ic.reset()
        ic.run()
        self.assertIn("0", mock_print.call_args[0][0])

    @mock.patch("intcode.print")
    @mock.patch("intcode.input")
    def test_jump_position(self, mock_input, mock_print):
        ic = IntCode("3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9")
        mock_input.return_value = 0
        ic.run()
        self.assertIn("0", mock_print.call_args[0][0])

        mock_input.return_value = 1
        ic.reset()
        ic.run()
        self.assertIn("1", mock_print.call_args[0][0])

    @mock.patch("intcode.print")
    @mock.patch("intcode.input")
    def test_jump_immediate(self, mock_input, mock_print):
        ic = IntCode("3,3,1105,-1,9,1101,0,0,12,4,12,99,1")
        mock_input.return_value = 0
        ic.run()
        self.assertIn("0", mock_print.call_args[0][0])

        mock_input.return_value = 1
        ic.reset()
        ic.run()
        self.assertIn("1", mock_print.call_args[0][0])

    @mock.patch("intcode.print")
    @mock.patch("intcode.input")
    def test_equality(self, mock_input, mock_print):
        ic = IntCode(
            """
3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99"""
        )
        mock_input.return_value = 7
        ic.run()
        self.assertIn("999", mock_print.call_args[0][0])

        mock_input.return_value = 8
        ic.reset()
        ic.run()
        self.assertIn("1000", mock_print.call_args[0][0])

        mock_input.return_value = 9
        ic.reset()
        ic.run()
        self.assertIn("1001", mock_print.call_args[0][0])
