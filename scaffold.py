from pathlib import Path


def solve(path: Path) -> None:
    text = path.read_text()
    solution_part_1 = 0
    solution_part_2 = 0



    print(solution_part_1)
    print(solution_part_2)


if __name__ == "__main__":
    solve(Path("input.txt"))