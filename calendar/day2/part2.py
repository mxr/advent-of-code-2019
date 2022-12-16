#!/usr/bin/env python3
from __future__ import annotations

from part1 import override_inputs
from part1 import read_inputs
from part1 import run_until_termination


def main() -> int:
    inputs = read_inputs()

    for noun in range(100):
        for verb in range(100):
            overridden = override_inputs(inputs, noun, verb)

            if run_until_termination(overridden) == 19690720:
                print(100 * noun + verb)
                return 0

    # should not be reached
    return 1


if __name__ == "__main__":
    exit(main())
