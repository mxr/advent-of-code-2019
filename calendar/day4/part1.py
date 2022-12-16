#!/usr/bin/env python3
from __future__ import annotations

import fileinput
from itertools import tee


def matches(num: int) -> bool:
    consecutive_equal = False

    digits1, digits2 = tee(str(num))
    next(digits2)
    for digit1, digit2 in zip(digits1, digits2):
        if int(digit2) < int(digit1):
            return False
        consecutive_equal |= digit1 == digit2

    return consecutive_equal


def main() -> int:
    count = 0
    n1, n2 = (int(n) for n in fileinput.input().readline().split("-"))
    for num in range(n1, n2):
        count += int(matches(num))

    print(count)

    return 0


if __name__ == "__main__":
    exit(main())
