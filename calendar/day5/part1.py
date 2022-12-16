#!/usr/bin/env python3
from __future__ import annotations

import fileinput
from contextlib import closing


def read_inputs() -> tuple[int, ...]:
    with closing(fileinput.input()) as f:
        return tuple(int(x) for x in f.readline().split(","))


def run_until_termination(inputs: list[int]) -> int:
    i = 0
    while True:
        op = int(str(inputs[i])[-2:])
        params = str(inputs[i])[:-2].zfill(3)

        if op == 1:
            inputs[inputs[i + 3]] = _value(inputs, i + 1, params[-1]) + _value(
                inputs, i + 2, params[-2]
            )
            i += 4
        elif op == 2:
            inputs[inputs[i + 3]] = _value(inputs, i + 1, params[-1]) * _value(
                inputs, i + 2, params[-2]
            )
            i += 4
        elif op == 3:
            inputs[inputs[i + 1]] = int(fileinput.input().readline())
            i += 2
        elif op == 4:
            print(_value(inputs, i + 1, params[-1]))
            i += 2
        else:
            assert op == 99
            return inputs[0]


def _value(inputs: list[int], i: int, mode: str) -> int:
    return inputs[inputs[i]] if mode == "0" else inputs[i]


def main() -> int:
    inputs = list(read_inputs())

    run_until_termination(inputs)

    return 0


if __name__ == "__main__":
    exit(main())
