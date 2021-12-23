from unittest import TestCase

from day_16 import parse, LiteralPacket, OperatorPacket, bits_to_int, int_to_bits


class Day16Test(TestCase):
    def test_bits_to_int(self):
        self.assertEqual(bits_to_int([0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1]), 2021)
        self.assertEqual(bits_to_int([1, 0, 1, 0]), 10)
        self.assertEqual(bits_to_int([0, 0, 0, 1, 0, 1, 0, 0]), 20)

    def test_int_to_bits(self):
        self.assertEqual(int_to_bits(2021), [0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1])
        self.assertEqual(int_to_bits(10), [1, 0, 1, 0])
        self.assertEqual(int_to_bits(20), [0, 0, 0, 1, 0, 1, 0, 0])

    def test_literal(self):
        packets = list(parse("D2FE28"))
        self.assertListEqual(list(parse("D2FE28")), [LiteralPacket(6, 4, 2021)])
        self.assertEqual(len(packets[0]), 21)

    def test_sub_packet_2(self):
        packets = list(parse("38006F45291200"))
        self.assertListEqual(
            packets,
            [
                OperatorPacket(
                    1,
                    6,
                    0,
                    [
                        LiteralPacket(6, 4, 10),
                        LiteralPacket(2, 4, 20),
                    ],
                )
            ],
        )
        self.assertEqual(len(packets[0]), 49)

    def test_sub_packet_3(self):
        packets = list(parse("EE00D40C823060"))
        self.assertListEqual(
            packets,
            [
                OperatorPacket(
                    7,
                    3,
                    1,
                    [
                        LiteralPacket(2, 4, 1),
                        LiteralPacket(4, 4, 2),
                        LiteralPacket(1, 4, 3),
                    ],
                )
            ],
        )
        self.assertEqual(len(packets[0]), 51)

    def test_nested_sub_packets(self):
        packets = list(parse("8A004A801A8002F478"))
        self.assertListEqual(
            packets,
            [
                OperatorPacket(
                    4,
                    2,
                    1,
                    [
                        OperatorPacket(
                            1,
                            2,
                            1,
                            [
                                OperatorPacket(
                                    5,
                                    2,
                                    0,
                                    [
                                        LiteralPacket(6, 4, 15),
                                    ],
                                )
                            ],
                        )
                    ],
                )
            ],
        )

    def test_value(self):
        data = {
            "D8005AC2A8F0": 1,
            "C200B40A82": 3,
            "04005AC33890": 54,
            "880086C3E88112": 7,
            "CE00C43D881120": 9,
            "F600BC2D8F": 0,
            "9C005AC2F8F0": 0,
            "9C0141080250320F1802104A08": 1,
        }
        for data_in, value in data.items():
            with self.subTest(data_in):
                packet = list(parse(data_in))[0]
                self.assertEqual(packet.value, value)
