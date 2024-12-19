import functools
from pathlib import Path

towels: list[str]


def solve(path: Path) -> None:
    global towels
    towels_raw, designs_raw = path.read_text().strip().split("\n\n")
    towels = [towel.strip() for towel in towels_raw.split(",")]
    designs: list[str] = [design.strip() for design in designs_raw.splitlines()]

    solution_part_1 = 0
    solution_part_2 = 0

    for i, design in enumerate(designs):
        if is_design_possible(design, towels):
            solution_part_1 += 1

        solution_part_2 += count_towel_arrangements(design)

    print(solution_part_1)
    print(solution_part_2)


def is_design_possible(design: str, towels: list[str]) -> bool:
    for towel in towels:
        if towel == design:
            return True

        if design.startswith(towel):
            remaining_designing = design.removeprefix(towel)
            if is_design_possible(remaining_designing, towels):
                return True

    return False


@functools.cache
def count_towel_arrangements(design: str) -> int:
    count = 0
    for towel in towels:
        if towel == design:
            count += 1

        if design.startswith(towel):
            remaining_designing = design.removeprefix(towel)
            count += count_towel_arrangements(remaining_designing)

    return count


if __name__ == "__main__":
    solve(Path("input.txt"))