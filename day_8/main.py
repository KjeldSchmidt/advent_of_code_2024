import itertools
from collections import defaultdict
from pathlib import Path
import numpy as np


def solve(path: Path) -> None:
    text = path.read_text()
    antennae = defaultdict(list)
    antinodes = set()
    resonant_antinodes = set()
    width = 0
    height = 0

    for row, line in enumerate(text.splitlines()):
        if line.strip() == "":
            continue

        height = row

        for col, char in enumerate(line):
            width = col
            if char == ".":
                continue


            antennae[char].append((row, col))

    for frequency, locations in antennae.items():
        for pair in itertools.product(locations, locations):
            a = pair[0]
            b = pair[1]
            if a == b:
                continue

            vector = np.array([a[0] - b[0], a[1] - b[1]])
            antinode_1 = b - vector
            antinode_2 = a + vector
            antinodes.add(tuple(antinode_1.tolist()))
            antinodes.add(tuple(antinode_2.tolist()))

            steps = 0
            while True:
                antinode_1 = b - vector*steps
                antinode_2 = a + vector*steps
                in_range = False

                if 0 <= antinode_1[0] <= height and 0 <= antinode_1[1] <= width:
                    resonant_antinodes.add(tuple(antinode_1.tolist()))
                    in_range = True

                if 0 <= antinode_2[0] <= height and 0 <= antinode_2[1] <= width:
                    resonant_antinodes.add(tuple(antinode_2.tolist()))
                    in_range = True

                steps += 1
                if not in_range:
                    break


    antinodes_in_grid = set()
    for antinode in antinodes:
        if not 0 <= antinode[0] <= height:
            continue

        if not 0 <= antinode[1] <= width:
            continue

        antinodes_in_grid.add(antinode)

    solution_part_1 = len(antinodes_in_grid)
    solution_part_2 = len(resonant_antinodes)


    print(solution_part_1)
    print(solution_part_2)


if __name__ == "__main__":
    solve(Path("input.txt"))