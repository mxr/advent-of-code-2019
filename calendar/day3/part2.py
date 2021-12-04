#!/usr/bin/env python3
import fileinput

from part1 import build_grid
from part1 import lay_path1
from part1 import lay_path2
from part1 import parse_path


def main() -> int:
    path1, path2 = (parse_path(rp) for rp in fileinput.input())
    grid, bounds = build_grid(path1, path2)

    origin_x, origin_y = abs(bounds.min_width), abs(bounds.min_height)

    lay_path1(grid, origin_x, origin_y, path1)
    lay_path2(grid, origin_x, origin_y, path2)

    min_steps = float("+inf")
    for row in grid:
        for cell in row:
            if cell is not None and cell.wire1 & cell.wire2:
                min_steps = min(min_steps, cell.count_wire1 + cell.count_wire2)

    print(min_steps)

    return 0


if __name__ == "__main__":
    exit(main())
