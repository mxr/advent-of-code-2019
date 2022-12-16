#!/usr/bin/env python3
from __future__ import annotations

import fileinput
from collections import Counter
from itertools import tee


def matches(num: int) -> bool:
    counts = Counter(str(num))

    digits1, digits2 = tee(str(num))
    next(digits2)

    consecutive_digits = set()
    for digit1, digit2 in zip(digits1, digits2):
        if int(digit2) < int(digit1):
            return False
        if digit1 == digit2:
            consecutive_digits.add(digit1)

    return any(counts[d] == 2 for d in consecutive_digits)


def main() -> int:
    count = 0
    n1, n2 = (int(n) for n in fileinput.input().readline().split("-"))
    for num in range(n1, n2):
        count += int(matches(num))

    print(count)

    return 0


if __name__ == "__main__":
    exit(main())
