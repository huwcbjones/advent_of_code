from enum import IntEnum
from functools import reduce
from math import floor
from typing import List, Optional


def flatten_2d_array(array: List[List[int]]) -> List[int]:
    return reduce(lambda x, y: x + y, array)


class Pixel(IntEnum):
    BLACK = 0
    WHITE = 1
    TRANSPARENT = 2


class Image:
    def __init__(self, data: str, width: int, height: int) -> None:
        self._width: int = width
        self._height: int = height
        self._checksum: Optional[int] = None
        self._image: Optional[str] = None

        number_of_layers = len(data) / (height * width)
        if number_of_layers != number_of_layers:
            raise ValueError("Image does not have a valid number of layers")
        self._number_of_layers: int = floor(number_of_layers)

        self._data: List[List[List[int]]] = [
            [
                [
                    int(data[x + width * y + width * height * layer])
                    for x in range(0, width)
                ]
                for y in range(0, height)
            ]
            for layer in range(0, self._number_of_layers)
        ]

    @property
    def height(self) -> int:
        return self._height

    @property
    def width(self) -> int:
        return self._width

    @property
    def number_of_layers(self) -> int:
        return self._number_of_layers

    @property
    def checksum(self) -> int:
        if self._checksum is None:
            self._checksum = self._calculate_checksum()
        return self._checksum

    @property
    def rendered_image(self):
        if self._image is None:
            self._image = self._render()
        return self._image

    def _calculate_checksum(self) -> int:
        # Get a list of Tuples[layer number, 0 count]
        zero_count = [
            (i, flatten_2d_array(layer).count(0)) for i, layer in enumerate(self._data)
        ]
        zero_count = sorted(zero_count, key=lambda x: x[1])
        layer_with_fewest_zeroes = self._data[zero_count[0][0]]

        flat_layer = flatten_2d_array(layer_with_fewest_zeroes)
        return flat_layer.count(1) * flat_layer.count(2)

    def _render(self) -> str:
        image: List[List[int]] = [
            [0 for __ in range(0, self.width)] for _ in range(0, self.height)
        ]
        for y in range(0, self.height):
            for x in range(0, self.width):
                for i, layer in enumerate(self._data):
                    pixel = layer[y][x]
                    if pixel != Pixel.TRANSPARENT:
                        image[y][x] = pixel
                        break

        return "\n".join(["".join([str(p) for p in row]) for row in image])


def part1(image: Image):
    print(image.checksum)
    assert image.checksum == 2193


def part2(image: Image):
    # Should output "YEHEF"
    print(image.rendered_image.replace("1", "█").replace("0", "░"))


def main():
    with open("day_08-input.txt", "r") as f:
        image = Image(f.read().strip(), 25, 6)
    part1(image)
    part2(image)


if __name__ == "__main__":
    main()
