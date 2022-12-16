#!/usr/bin/env python3
from __future__ import annotations

import fileinput
import itertools
from operator import add
from operator import mul

CHUNK_SIZE = 4


def read_inputs() -> tuple[int, ...]:
    line = next(fileinput.input())
    return tuple(int(x) for x in line.split(","))


def override_inputs(inputs: tuple[int, ...], at1: int, at2: int) -> list[int]:
    return list(itertools.chain((inputs[0],), (at1, at2), inputs[3:]))


def run_until_termination(inputs: list[int]) -> int:
    for i in range(0, len(inputs), CHUNK_SIZE):
        op, i1, i2, out, *_ = inputs[i : i + CHUNK_SIZE]
        if op == 99:
            return inputs[0]

        inputs[out] = (add if op == 1 else mul)(inputs[i1], inputs[i2])

    raise ValueError("should not be reached")


def main() -> int:
    inputs = read_inputs()

    # > before running the program, replace position 1 with the value 12 and
    # > replace position 2 with the value 2.
    overridden = override_inputs(inputs, 12, 2)

    print(run_until_termination(overridden))

    return 0


if __name__ == "__main__":
    exit(main())
