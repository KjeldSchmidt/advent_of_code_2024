import functools
import itertools
from pathlib import Path
import numpy as np

heights: np.ndarray

def solve(path: Path) -> None:
    global heights
    text = path.read_text()
    heights = np.array([[-1 if char == "." else int(char) for char in line] for line in text.strip().splitlines()])

    solution_part_1 = 0
    solution_part_2 = 0

    height = heights.shape[0]
    width = heights.shape[1]
    for row, col in itertools.product(range(height), range(width)):
        if heights[row, col] == 0:
            distinct_trails = count_trails(row, col)
            reachable_peaks = get_reachable_peaks(row, col)
            solution_part_1 += len(reachable_peaks)
            solution_part_2 += distinct_trails

    print(solution_part_1)
    print(solution_part_2)


def count_trails(row: int, col: int) -> int:
    current_height = heights[row, col]
    height = heights.shape[0]
    width = heights.shape[1]
    if current_height == 9:
        return 1

    trails = 0

    if row > 0 and heights[row - 1, col] == current_height + 1:
        trail_score = count_trails(row - 1, col)
        print(f"got {trail_score} at {row}, {col}, height {height}")
        trails += trail_score

    if row < height - 1 and heights[row + 1, col] == current_height + 1:
        trail_score = count_trails(row + 1, col)
        print(f"got {trail_score} at {row}, {col}, height {height}")
        trails += trail_score

    if col > 0 and heights[row, col - 1] == current_height + 1:
        trail_score = count_trails(row, col - 1)
        print(f"got {trail_score} at {row}, {col}, height {height}")
        trails += trail_score

    if col < width - 1 and heights[row, col + 1] == current_height + 1:
        trail_score = count_trails(row, col + 1)
        print(f"got {trail_score} at {row}, {col}, height {height}")
        trails += trail_score

    return trails


def get_reachable_peaks(row: int, col: int) -> set[tuple[int, int]]:
    current_height = heights[row, col]
    height = heights.shape[0]
    width = heights.shape[1]
    if current_height == 9:
        return {(row, col)}

    reachable_peaks = set()

    if row > 0 and heights[row - 1, col] == current_height + 1:
        new_peaks = get_reachable_peaks(row - 1, col)
        reachable_peaks.update(new_peaks)

    if row < height - 1 and heights[row + 1, col] == current_height + 1:
        new_peaks = get_reachable_peaks(row + 1, col)
        reachable_peaks.update(new_peaks)

    if col > 0 and heights[row, col - 1] == current_height + 1:
        new_peaks = get_reachable_peaks(row, col - 1)
        reachable_peaks.update(new_peaks)

    if col < width - 1 and heights[row, col + 1] == current_height + 1:
        new_peaks = get_reachable_peaks(row, col + 1)
        reachable_peaks.update(new_peaks)

    return reachable_peaks


if __name__ == "__main__":
    solve(Path("input.txt"))