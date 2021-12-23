from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
from functools import cached_property
from math import prod
from pathlib import Path
from typing import Iterable

BITS = list[int]
DECODE_MAP: dict[str, tuple[int, int, int, int]] = {
    "0": (0, 0, 0, 0),
    "1": (0, 0, 0, 1),
    "2": (0, 0, 1, 0),
    "3": (0, 0, 1, 1),
    "4": (0, 1, 0, 0),
    "5": (0, 1, 0, 1),
    "6": (0, 1, 1, 0),
    "7": (0, 1, 1, 1),
    "8": (1, 0, 0, 0),
    "9": (1, 0, 0, 1),
    "A": (1, 0, 1, 0),
    "B": (1, 0, 1, 1),
    "C": (1, 1, 0, 0),
    "D": (1, 1, 0, 1),
    "E": (1, 1, 1, 0),
    "F": (1, 1, 1, 1),
}


def bits_to_int(bits: list[int]) -> int:
    return sum(2 ** i if v else 0 for i, v in enumerate(reversed(bits)))


def int_to_bits(number: int) -> list[int]:
    bits = [int(i) for i in f"{number:b}"]
    modulo = len(bits) % 4
    if modulo == 0:
        return bits
    return [0] * (4 - modulo) + bits


class Type(IntEnum):
    SUM = 0
    PRODUCT = 1
    MINIMUM = 2
    MAXIMUM = 3
    LITERAL = 4
    GREATER_THAN = 5
    LESS_THAN = 6
    EQUAL = 7


@dataclass
class Packet:
    version: int
    type: int

    @property
    def value(self) -> int:
        raise NotImplementedError()

    def __len__(self):
        return 6


@dataclass
class LiteralPacket(Packet):
    _value: int

    @cached_property
    def value(self) -> int:
        return self._value

    def __len__(self):
        return super().__len__() + (5 * len(int_to_bits(self._value)) // 4)


@dataclass
class OperatorPacket(Packet):
    length_type_id: int
    sub_packets: list[Packet]

    @cached_property
    def value(self) -> int:
        match self.type:
            case Type.SUM:
                return sum(p.value for p in self.sub_packets)
            case Type.PRODUCT:
                return prod(p.value for p in self.sub_packets)
            case Type.MINIMUM:
                return min(p.value for p in self.sub_packets)
            case Type.MAXIMUM:
                return max(p.value for p in self.sub_packets)
            case Type.GREATER_THAN:
                return int(self.sub_packets[0].value > self.sub_packets[1].value)
            case Type.LESS_THAN:
                return int(self.sub_packets[0].value < self.sub_packets[1].value)
            case Type.EQUAL:
                return int(self.sub_packets[0].value == self.sub_packets[1].value)

    def __len__(self):
        sub_packet_len = sum(len(p) for p in self.sub_packets)
        header_len = 1 + (15 if self.length_type_id == 0 else 11)
        return super().__len__() + header_len + sub_packet_len


def decode(transmission: str) -> BITS:
    def _decode() -> Iterable[int]:
        for char in transmission:
            yield from DECODE_MAP[char]

    return list(_decode())


def parse(transmission: str | BITS) -> Iterable[Packet]:
    if isinstance(transmission, str):
        data = decode(transmission)
    else:
        data = transmission

    version: int | None = None
    type_id: int | None = None
    while data:
        # Parse version/type_ID
        if version is None:
            version, data = bits_to_int(data[0:3]), data[3:]
        if type_id is None:
            type_id, data = Type(bits_to_int(data[0:3])), data[3:]

        # Parse literal
        if type_id == Type.LITERAL:
            literal = []
            while data[0] != 0:
                literal.extend(data[1:5])
                data = data[5:]
            literal.extend(data[1:5])
            data = data[5:]
            yield LiteralPacket(version, type_id, bits_to_int(literal))

        # Parse non-literal packet
        else:
            length_type_id, data = data[0], data[1:]
            packet = OperatorPacket(version, type_id, length_type_id, [])

            if length_type_id == 0:
                sub_packet_length, data = bits_to_int(data[0:15]), data[15:]
                for sub_packet in parse(data[:sub_packet_length]):
                    packet.sub_packets.append(sub_packet)
                data = data[sub_packet_length:]

            elif length_type_id == 1:
                sub_packet_count, data = bits_to_int(data[0:11]), data[11:]
                parser = iter(parse(data))
                for _ in range(sub_packet_count):
                    sub_packet = next(parser)
                    packet.sub_packets.append(sub_packet)
                    data = data[len(sub_packet) :]

            else:
                raise Exception(f"Invalid length_type_id {length_type_id}")

            yield packet

        version = type_id = None
        if not any(data):
            break


def version_sum(packets: list[Packet]) -> int:
    return sum(
        p.version + version_sum(p.sub_packets)
        if isinstance(p, OperatorPacket)
        else p.version
        for p in packets
    )


def main():
    with Path(__file__).parent.joinpath("day_16-input.txt").open("r") as input_f:
        transmission = input_f.readline().strip()
    packets = list(parse(transmission))

    print("Part1: ", version_sum(packets))
    print("Part1: ", packets[0].value)


if __name__ == "__main__":
    main()
