from pathlib import Path
import numpy as np


directions = {
    "^": np.array([-1, 0]),
    "v": np.array([1, 0]),
    ">": np.array([0, 1]),
    "<": np.array([0, -1]),
}


def solve_part_1(path: Path) -> None:
    grid, moves = path.read_text().strip().split("\n\n")
    grid = np.array([[block for block in line] for line in grid.split("\n")])

    moves = "".join(moves.split("\n"))

    make_all_moves_part_1(grid, moves)
    print(calc_score_part_1(grid))


def solve_part_2(path: Path) -> None:
    grid_t, moves = path.read_text().strip().split("\n\n")

    moves = "".join(moves.split("\n"))

    grid_t: str = grid_t.replace("#", "##")
    grid_t: str = grid_t.replace("O", "[]")
    grid_t: str = grid_t.replace(".", "..")
    grid_t: str = grid_t.replace("@", "@.")
    grid = np.array([[block for block in line] for line in grid_t.split("\n")])

    show_board(grid)

    for move in moves:
        d = directions[move]

        r = np.argwhere(grid == "@").flatten()
        pushing_items = [r]
        pushed_items = []

        chain_hits_wall = False
        while pushing_items:
            pushing_item = pushing_items.pop()
            pushed_items.append((pushing_item, grid[*pushing_item]))
            pushed_items_coordinates = [yx for yx, _ in pushed_items]
            pushing_candidate = (pushing_item + d)

            if grid[*pushing_candidate] == "#":
                chain_hits_wall = True
                break

            if grid[*pushing_candidate] == "[":
                pushing_items.append(pushing_candidate)
                right_side = pushing_candidate + [0, 1]
                full_box_has_already_been_pushed = any(np.array_equal(right_side, v) for v in pushed_items_coordinates)
                if not full_box_has_already_been_pushed:
                    pushing_items.append(pushing_candidate + [0, 1])

            if grid[*pushing_candidate] == "]":
                pushing_items.append(pushing_candidate)
                left_side = pushing_candidate + [0, -1]
                full_box_has_already_been_pushed = any(np.array_equal(left_side, v) for v in pushed_items_coordinates)
                if not full_box_has_already_been_pushed:
                    pushing_items.append(pushing_candidate + [0, -1])

        if chain_hits_wall:
            continue

        new_grid = grid.copy()

        for coordinates, _ in pushed_items:
            new_grid[*coordinates] = "."

        for coordinates, thing in pushed_items:
            new_grid[*(coordinates+d)] = thing

        grid = new_grid

    print(calc_score_part_2(grid))


def make_all_moves_part_1(grid: np.ndarray, moves: str) -> None:
    for move in moves:
        r = np.argwhere(grid == "@").flatten()
        d = directions[move]
        t = r.copy()
        while grid[*(t+d)] not in ["#", "."]:
            t += d

        if move in [">", "v"]:
            moved_slice = grid[r[0]:t[0]+1, r[1]:t[1]+1]
        if move in ["^", "<"]:
            moved_slice = grid[t[0]:r[0]+1, t[1]:r[1]+1]

        if grid[*(t+d)] == "#":
            continue

        if move in [">", "v"]:
            grid[r[0]+d[0]: t[0]+d[0]+1, r[1]+d[1] : t[1]+d[1]+1] = moved_slice
        if move in ["^", "<"]:
            grid[t[0]+d[0]: r[0]+d[0]+1, t[1]+d[1] : r[1]+d[1]+1] = moved_slice

        grid[*r] = "."


def calc_score_part_1(grid: np.ndarray) -> int:
    boxes = np.argwhere(grid == "O")
    score = 0
    for box in boxes:
        score += 100*box[0] + box[1]
    return score


def calc_score_part_2(grid: np.ndarray) -> int:
    boxes = np.argwhere(grid == "[")
    score = 0
    for box in boxes:
        score += 100*box[0] + box[1]
    return score


def show_board(grid: np.ndarray) -> None:
    height, width = grid.shape
    for y in range(height):
        for x in range(width):
            display = grid[y, x]
            if display == ".":
                display = " "
            print(display, end="")
        print()


if __name__ == "__main__":
    solve_part_1(Path("input.txt"))
    solve_part_2(Path("input.txt"))