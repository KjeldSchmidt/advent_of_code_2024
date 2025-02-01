import itertools
from pathlib import Path
import numpy as np


def solve(path: Path) -> None:
    keys_and_locks_raw: list[str] = path.read_text().strip().split("\n\n")
    keys = []
    locks = []

    for key_or_lock in keys_and_locks_raw:
        array = np.array([[0 if c == "." else 1 for c in line] for line in key_or_lock.splitlines()])
        heights = array.sum(axis=0)
        heights -= 1
        if array[0][0] == 0:
            keys.append(heights)
        elif array[0][0] == 1:
            locks.append(heights)
        else:
            raise AssertionError("Assumption about input broken")

    solution_part_1 = 0
    for key, lock in itertools.product(keys, locks):
        if not np.any(key + lock > 5):
            solution_part_1 += 1

    solution_part_2 = 0

    print(solution_part_1)
    print(solution_part_2)


if __name__ == "__main__":
    solve(Path("input.txt"))