#!/usr/bin/env python3
import itertools
from typing import List
from typing import Tuple

from part1 import build_orbits
from part1 import Primary
from part1 import read_inputs


def overlap_distance(root: Primary, name1: str, name2: str) -> int:
    paths = _paths(root)

    path1 = [p for p in paths if p[-1] == name1][0]
    path2 = [p for p in paths if p[-1] == name2][0]

    common_i = 0
    for p1, p2 in zip(path1, path2):
        if p1 != p2:
            break

        common_i += 1

    dist_from_common_to_name1 = len(path1) - common_i
    dist_from_common_to_name2 = len(path2) - common_i

    return dist_from_common_to_name1 + dist_from_common_to_name2 - 2


def _paths(root: Primary) -> List[Tuple[str, ...]]:
    return (
        [
            tuple(itertools.chain((root.name,), p))
            for s in root.satellites
            for p in _paths(s)
        ]
        if root.satellites
        else [(root.name,)]
    )


def main() -> int:
    inputs = read_inputs()

    root = build_orbits(inputs)

    distance = overlap_distance(root, "YOU", "SAN")

    print(distance)

    return 0


if __name__ == "__main__":
    exit(main())
