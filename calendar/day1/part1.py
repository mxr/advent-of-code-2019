#!/usr/bin/env python3
import fileinput


def fuel(mass: int) -> int:
    return int(mass / 3 - 2)


def main() -> int:
    total = 0
    for line in fileinput.input():
        total += fuel(int(line))

    print(total)

    return 0


if __name__ == "__main__":
    exit(main())
