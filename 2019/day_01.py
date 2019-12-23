from math import floor


def fuel(mass):
    return floor(mass / 3) - 2


def total_fuel(mass):
    total_fuel = 0
    fuel_for_mass = fuel(mass)
    while fuel_for_mass > 0:
        total_fuel += fuel_for_mass
        fuel_for_mass = fuel(fuel_for_mass)
    return total_fuel


def part1(f):
    fuel_mass = sum([fuel(int(m.strip())) for m in f.readlines() if m.strip()])
    print(f"Total Fuel Mass: {fuel_mass}")


def part2(f):
    fuel_mass = sum([total_fuel(int(m.strip())) for m in f.readlines() if m.strip()])
    print(f"Total Fuel Mass: {fuel_mass}")


if __name__ == "__main__":
    with open("day_01-input.txt", "r") as f:
        part1(f)
        f.seek(0)
        part2(f)
