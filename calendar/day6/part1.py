#!/usr/bin/env python3
import fileinput
from contextlib import closing
from dataclasses import dataclass
from typing import Generator
from typing import List
from typing import Optional
from typing import Tuple


@dataclass
class Primary:
    name: str
    satellites: List["Primary"]
    depth: int = 0

    def __hash__(self) -> int:
        return hash(self.name)


def read_inputs() -> Tuple[Tuple[str, str], ...]:
    def _read() -> Generator[Tuple[str, str], None, None]:
        with closing(fileinput.input()) as f:
            for line in f:
                primary, _, satellite = line.strip().partition(")")
                yield primary, satellite

    return tuple(_read())


def build_orbits(inputs: Tuple[Tuple[str, str], ...]) -> Primary:
    assert inputs

    root = Primary(inputs[0][0], [Primary(inputs[0][1], [])])

    to_process = set(inputs[1:])
    while to_process:
        to_delete = set()
        for (name, sat_name) in to_process:
            if sat_name == root.name:
                root = Primary(name, [root])
                to_delete.add((name, sat_name))
                continue

            leaf = _find_leaf(root, name)
            if leaf:
                leaf.satellites.append(Primary(sat_name, []))
                to_delete.add((name, sat_name))

        to_process.difference_update(to_delete)

    return root


def _find_leaf(root: Primary, name: str) -> Optional[Primary]:
    if root.name == name:
        return root

    for sat in root.satellites:
        leaf = _find_leaf(sat, name)
        if leaf:
            return leaf

    return None


def hydrate_depths(root: Primary, parent_depth: int = -1) -> None:
    root.depth = parent_depth + 1
    for s in root.satellites:
        hydrate_depths(s, root.depth)


def total_depths(root: Primary) -> int:
    return root.depth + sum(total_depths(s) for s in root.satellites)


def main() -> int:
    inputs = read_inputs()

    root = build_orbits(inputs)

    hydrate_depths(root)
    print(total_depths(root))

    return 0


if __name__ == "__main__":
    exit(main())
