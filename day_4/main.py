import re
from pathlib import Path
import numpy as np

def solve_part_1(path: Path) -> None:
    text = path.read_text()
    array = np.array([list(row) for row in text.splitlines()])

    total = 0
    for col in range(array.shape[1]):
        total += count_xmas(array[:,col])

    for row in range(array.shape[0]):
        total += count_xmas(array[row])

    for offset in range(-array.shape[0] + 1, array.shape[1]):
        total += count_xmas(np.diagonal(array, offset=offset))

    flipped_array = np.fliplr(array)
    for offset in range(-flipped_array.shape[0] + 1, flipped_array.shape[1]):
        total += count_xmas(np.diagonal(flipped_array, offset=offset))

    print(total)


def solve_part_2(path: Path) -> None:
    text = path.read_text()
    array = np.array([list(row) for row in text.splitlines()])

    rows, cols = array.shape

    total = 0
    for i in range(rows - 2):
        for j in range(cols - 2):
            window = array[i:i+3, j:j+3]
            if is_mas_cross(window):
                total += 1

    print(total)


def is_mas_cross(window: np.ndarray) -> bool:
    main_diagonal = "".join(window.diagonal())
    anti_diagonal = "".join(np.fliplr(window).diagonal())

    return main_diagonal in ["MAS", "SAM"] and anti_diagonal in ["MAS", "SAM"]



def count_xmas(line: np.ndarray) -> int:
    xmas_forwards = len(re.findall("XMAS", "".join(line)))
    xmas_backwards = len(re.findall("XMAS", "".join(line[::-1])))
    return xmas_forwards + xmas_backwards


solve_part_1(Path("input.txt"))
solve_part_2(Path("input.txt"))