from enum import Enum, auto
from pathlib import Path
from typing import Generator

from scipy.cluster.hierarchy import DisjointSet
import numpy as np

regions = DisjointSet()


def solve(path: Path) -> None:
    text = path.read_text().strip().splitlines()
    garden = np.array([[char for char in line] for line in text])
    height, width = garden.shape

    for row in range(height):
        for col in range(width):
            regions.add((row, col))

    for row in range(height):
        for col in range(width):
            for row_n, col_n in four_neighbourhood(row, col, height, width):
                if garden[row][col] == garden[row_n][col_n]:
                    regions.merge((row, col), (row_n, col_n))

    region: set[tuple[int, int]]
    perimeter_cost = 0
    sides_cost = 0
    for region in regions.subsets():
        area = len(region)
        perimeter = calculate_region_perimeter(region)
        number_of_sides = calculate_number_of_sides(region)
        perimeter_cost += area * perimeter
        sides_cost += area * number_of_sides

    print(f"Solution Part 1: {perimeter_cost}")
    print(f"Solution Part 2: {sides_cost}")


def calculate_region_perimeter(region: set[tuple[int, int]]) -> int:
    perimeter = len(region) * 4

    for plot_y, plot_x in region:
        for neighbor_plot in four_neighbourhood(plot_y, plot_x):
            if neighbor_plot in region:
                perimeter -= 1

    return perimeter


class WallSide(Enum):
    Top = auto()
    Right = auto()
    Bottom = auto()
    Left = auto()


def calculate_number_of_sides(region: set[tuple[int, int]]) -> int:
    side_sets = {
        WallSide.Bottom: DisjointSet(),
        WallSide.Right: DisjointSet(),
        WallSide.Top: DisjointSet(),
        WallSide.Left: DisjointSet(),
    }

    for plot_y, plot_x in region:
        if not (plot_y+1, plot_x) in region:
            side_sets[WallSide.Bottom].add((plot_y, plot_x))

        if not (plot_y, plot_x+1) in region:
            side_sets[WallSide.Right].add((plot_y, plot_x))

        if not (plot_y-1, plot_x) in region:
            side_sets[WallSide.Top].add((plot_y, plot_x))

        if not (plot_y, plot_x-1) in region:
            side_sets[WallSide.Left].add((plot_y, plot_x))

    for vertical_side in [side_sets[WallSide.Left], side_sets[WallSide.Right]]:
        for plot_y, plot_x in vertical_side:
            if (plot_y+1, plot_x) in vertical_side:
                vertical_side.merge((plot_y, plot_x), (plot_y+1, plot_x))

            if (plot_y-1, plot_x) in vertical_side:
                vertical_side.merge((plot_y, plot_x), (plot_y-1, plot_x))

    for horizontal_side in [side_sets[WallSide.Top], side_sets[WallSide.Bottom]]:
        for plot_y, plot_x in horizontal_side:
            if (plot_y, plot_x+1) in horizontal_side:
                horizontal_side.merge((plot_y, plot_x), (plot_y, plot_x+1))

            if (plot_y, plot_x-1) in horizontal_side:
                horizontal_side.merge((plot_y, plot_x), (plot_y, plot_x-1))

    sides_count = 0
    for side_set in side_sets.values():
        sides_count += len(side_set.subsets())

    return sides_count


def four_neighbourhood(row, col, height=None, width=None) -> Generator[tuple[int, int], None, None]:
    if height is None or row < height-1:
        yield row+1, col

    if width is None or col < width-1:
        yield row, col+1

    if height is None or row > 0:
        yield row-1, col

    if width is None or col > 0:
        yield row, col-1


if __name__ == "__main__":
    solve(Path("input.txt"))