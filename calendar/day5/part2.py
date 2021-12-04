#!/usr/bin/env python3
import fileinput
from typing import List
from typing import NamedTuple
from typing import Optional

from part1 import read_inputs


class OpArgs(NamedTuple):
    val1: int
    val2: int
    i: int


class OpRet(NamedTuple):
    ret: Optional[int]
    ret_i: Optional[int]
    new_i: int


def add(args: OpArgs) -> OpRet:
    return OpRet(args.val1 + args.val2, args.i + 3, args.i + 4)


def mul(args: OpArgs) -> OpRet:
    return OpRet(args.val1 * args.val2, args.i + 3, args.i + 4)


def read(args: OpArgs) -> OpRet:
    return OpRet(int(fileinput.input().readline()), args.i + 1, args.i + 2)


def echo(args: OpArgs) -> OpRet:
    print(args.val1)
    return OpRet(None, None, args.i + 2)


def jt(args: OpArgs) -> OpRet:
    return OpRet(None, None, args.i + 3 if args.val1 == 0 else args.val2)


def jf(args: OpArgs) -> OpRet:
    return OpRet(None, None, args.val2 if args.val1 == 0 else args.i + 3)


def lt(args: OpArgs) -> OpRet:
    return OpRet(int(args.val1 < args.val2), args.i + 3, args.i + 4)


def eq(args: OpArgs) -> OpRet:
    return OpRet(int(args.val1 == args.val2), args.i + 3, args.i + 4)


OP_TO_FUNC = {
    1: add,
    2: mul,
    3: read,
    4: echo,
    5: jt,
    6: jf,
    7: lt,
    8: eq,
}


def run_until_termination(inputs: List[int]) -> int:
    i = 0
    while inputs[i] != 99:
        padded = str(inputs[i]).zfill(5)
        op = int(padded[-2:])
        params = padded[:-2]

        val1 = _maybe_value(inputs, i + 1, params[-1])
        val2 = _maybe_value(inputs, i + 2, params[-2])

        args = OpArgs(val1, val2, i)

        ret = OP_TO_FUNC[op](args)

        if ret.ret_i is not None:
            assert ret.ret is not None
            inputs[inputs[ret.ret_i]] = ret.ret

        i = ret.new_i

    return inputs[0]


def _maybe_value(inputs: List[int], i: int, mode: str) -> int:
    try:
        return inputs[inputs[i]] if mode == "0" else inputs[i]
    except IndexError:
        return 0


def main() -> int:
    inputs = list(read_inputs())

    run_until_termination(inputs)

    return 0


if __name__ == "__main__":
    exit(main())
