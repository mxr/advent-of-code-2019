#!/usr/bin/env python3
import fileinput

from part1 import fuel


def main() -> int:
    total = 0
    for line in fileinput.input():
        this_fuel = fuel(int(line))
        while this_fuel >= 0:
            total += this_fuel
            this_fuel = fuel(this_fuel)

    print(total)

    return 0


if __name__ == "__main__":
    exit(main())
