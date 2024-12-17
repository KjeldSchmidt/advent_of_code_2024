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

    grid_t: str = path.read_text().strip().split("\n\n")[0]
    grid = np.array([[block for block in line] for line in grid_t.split("\n")])

    stretch = np.array([1, 2])
    robot = (np.argwhere(grid == "@") * stretch)
    walls = (np.argwhere(grid == "#") * stretch)
    boxes = (np.argwhere(grid == "O") * stretch)
    show_board_part_2(robot, walls, boxes)

    for move in moves:
        print()
        print()
        print(move)
        d = directions[move]
        if np.any((walls == robot+d).all(axis=1)):
            print("No move, wall in the way, sorry")
        elif np.any((boxes == robot+d).all(axis=1)):
            print("Can't handle the stress of pushing from the left yet, sorry")
            raise NotImplementedError()
        elif np.any(((boxes + [0, 1]) == robot+d).all(axis=1)):
            print("Can't handle the stress of pushing from the right yet, sorry")
            pushing_items = [robot]
            while pushing_items != []:
                pass

            raise NotImplementedError()
        else:
            print("Moving, bitches!")
            robot += d
        show_board_part_2(robot, walls, boxes)


def show_board_part_2(robot, walls, boxes):
    width = np.max(walls)
    height = width // 2
    for y in range(height + 1):
        for x in range(width + 2):
            char_to_print = " "
            if np.any(([y, x] == robot).all(axis=1)):
                char_to_print = "@"
            if np.any(([y, x] == walls).all(axis=1)) or np.any(([y, x-1] == walls).all(axis=1)):
                char_to_print = "#"
            if np.any(([y, x] == boxes).all(axis=1)):
                char_to_print = "["
            if np.any(([y, x-1] == boxes).all(axis=1)):
                char_to_print = "]"

            print(char_to_print, end="")
        print()


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


def show_board_part_1(grid: np.ndarray) -> None:
    height, width = grid.shape
    for y in range(height):
        for x in range(width):
            display = grid[y, x]
            if display == ".":
                display = " "
            print(display, end="")
        print()


if __name__ == "__main__":
    solve_part_1(Path("input-small.txt"))
    solve_part_2(Path("input-small.txt"))