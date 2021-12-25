from collections import defaultdict
from itertools import product
from pathlib import Path

Image = dict[int, dict[int, int]]


def print_image(image: Image):
    min_y = min(image.keys())
    max_y = max(image.keys())
    min_x = min(min(r.keys()) for r in image.values())
    max_x = max(max(r.keys()) for r in image.values())
    for y in range(min_y, max_y + 1):
        print("".join("#" if image[y][x] else "." for x in range(min_x, max_x + 1)))


def enhance(image: Image, enhancement: list[bool], steps: int = 1) -> Image:
    default = 0
    for _ in range(steps):
        new_image = defaultdict(lambda: defaultdict(lambda: default))
        points = {
            (x + d_x, y + d_y)
            for y, row in image.items()
            for x in row.keys()
            for d_y, d_x in product([-1, 0, 1], repeat=2)
        }
        for x, y in points:
            number = 0
            for d_y, d_x in product([-1, 0, 1], repeat=2):
                number <<= 1
                number += image[y + d_y][x + d_x]
            new_image[y][x] = enhancement[number]
        image = new_image
        default = enhancement[-default]
    return image


def sum_lit_pixels(image: Image) -> int:
    return sum(sum(r.values()) for r in image.values())


def main():
    with Path(__file__).parent.joinpath("day_20-input.txt").open("r") as input_f:
        enhancement: list[bool] = [c == "#" for c in input_f.readline().strip()]
        input_f.readline()

        image: Image = defaultdict(lambda: defaultdict(int))
        for y, line in enumerate(input_f.readlines()):
            for x, i in enumerate(line.strip()):
                image[y][x] = int(i == "#")

        print("Part1: ", sum_lit_pixels(enhance(image, enhancement, 2)))
        print("Part2: ", sum_lit_pixels(enhance(image, enhancement, 50)))


if __name__ == "__main__":
    main()
