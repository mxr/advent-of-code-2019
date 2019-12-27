#!/usr/bin/env python3
import fileinput
import os
from distutils.util import strtobool
from typing import Callable
from typing import Iterable
from typing import List
from typing import NamedTuple
from typing import Optional
from typing import Tuple

from dataclasses import dataclass

Step = NamedTuple("Step", (("direction", str), ("amount", int)))
Bounds = NamedTuple(
    "Bounds",
    (
        ("min_width", int),
        ("min_height", int,),
        ("max_width", int),
        ("max_height", int,),
    ),
)


@dataclass
class Cell:
    wire1: bool
    wire2: bool


def parse_path(raw_path: str) -> List[Step]:
    return [Step(s[0], int(s[1:])) for s in raw_path.split(",")]


def build_grid(
    path1: Iterable[Step], path2: Iterable[Step]
) -> Tuple[List[List[Optional[Cell]]], Bounds]:
    b1 = count_bounds(path1)
    b2 = count_bounds(path2)

    bounds = Bounds(
        min_width=min(b1.min_width, b2.min_width),
        min_height=min(b1.min_height, b2.min_height),
        max_width=max(b1.max_width, b2.max_width),
        max_height=max(b1.max_height, b2.max_height),
    )
    grid: List[List[Optional[Cell]]] = []
    for _ in range(bounds.max_height - bounds.min_height + 1):
        grid.append([None for _ in range(bounds.max_width - bounds.min_width + 1)])

    return grid, bounds


def count_bounds(path: Iterable[Step]) -> Bounds:
    min_width, min_height, max_width, max_height = 0, 0, 0, 0

    width, height, width, height = 0, 0, 0, 0
    for s in path:
        if s.direction == "R":
            width += s.amount
        elif s.direction == "L":
            width -= s.amount
        elif s.direction == "U":
            height += s.amount
        elif s.direction == "D":
            height -= s.amount

        min_width = min(width, min_width)
        min_height = min(height, min_height)
        max_width = max(width, max_width)
        max_height = max(height, max_height)

    return Bounds(
        min_width=min_width,
        min_height=min_height,
        max_width=max_width,
        max_height=max_height,
    )


def lay_path1(
    grid: List[List[Optional[Cell]]], origin_x: int, origin_y: int, path: Iterable[Step]
) -> None:
    _lay_path(grid, origin_x, origin_y, path, _place_wire_path1)


def lay_path2(
    grid: List[List[Optional[Cell]]], origin_x: int, origin_y: int, path: Iterable[Step]
) -> None:
    _lay_path(grid, origin_x, origin_y, path, _place_wire_path2)


def _lay_path(
    grid: List[List[Optional[Cell]]],
    origin_x: int,
    origin_y: int,
    path: Iterable[Step],
    which: Callable[[List[List[Optional[Cell]]], int, int], None],
) -> None:
    x, y = origin_x, origin_y
    for s in path:
        if s.direction == "R":
            for i in range(1, s.amount + 1):
                which(grid, x + i, y)
            x += s.amount

        elif s.direction == "L":
            for i in range(1, s.amount + 1):
                which(grid, x - i, y)
            x -= s.amount

        elif s.direction == "U":
            for i in range(1, s.amount + 1):
                which(grid, x, y + i)
            y += s.amount

        elif s.direction == "D":
            for i in range(1, s.amount + 1):
                which(grid, x, y - i)
            y -= s.amount


def _place_wire_path1(grid: List[List[Optional[Cell]]], x: int, y: int) -> None:
    cell = grid[y][x]
    if cell is None:
        grid[y][x] = Cell(True, False)


def _place_wire_path2(grid: List[List[Optional[Cell]]], x: int, y: int) -> None:
    cell = grid[y][x]
    if cell is None:
        grid[y][x] = Cell(False, True)
    else:
        cell.wire2 = True


def _debug() -> bool:
    return strtobool(os.getenv("DEBUG", "false"))


def main() -> int:
    path1, path2 = [parse_path(rp) for rp in fileinput.input()]
    grid, bounds = build_grid(path1, path2)

    origin_x, origin_y = abs(bounds.min_width), abs(bounds.min_height)

    lay_path1(grid, origin_x, origin_y, path1)
    lay_path2(grid, origin_x, origin_y, path2)

    if _debug():
        y = bounds.max_height
        while y >= bounds.min_height:
            row = grid[y]
            print(
                "".join(
                    "o"
                    if y == 0 and i == 0
                    else "."
                    if c is None
                    else "1"
                    if c.wire1 and not c.wire2
                    else "2"
                    if c.wire2 and not c.wire1
                    else "x"
                    for i, c in enumerate(row)
                )
            )
            y -= 1

    min_dist = bounds.max_height + bounds.max_width
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell is not None and cell.wire1 & cell.wire2:
                min_dist = min(min_dist, abs(y - origin_y) + abs(x - origin_x))

    print(min_dist)

    return 0


if __name__ == "__main__":
    exit(main())
