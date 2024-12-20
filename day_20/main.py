import itertools
from pathlib import Path

import numpy as np


def solve(path: Path) -> None:
    text = path.read_text().strip()
    maze = np.array([[cell for cell in line] for line in text.splitlines()])
    height, width = maze.shape

    start: np.array
    end: np.array
    for y, x in itertools.product(range(height), range(width)):
        if maze[y][x] == "E":
            end = np.array([y, x])

        if maze[y][x] == "S":
            start = np.array([y, x])

    path = [start]
    current_pos = start
    while not np.all(current_pos == end):
        for neighbour in four_neighbourhood(current_pos[0], current_pos[1], height, width):
            if len(path) > 1 and np.all(neighbour == path[-2]):
                continue

            if maze[*neighbour] in [".", "E"]:
                path.append(neighbour)
                current_pos = path[-1]
                break

    path_indices = {tuple(point): i for i, point in enumerate(path)}
    solution_part_1 = 0
    print("This might take a minute, don't worry, answer is coming soon.")
    for start_index, node in enumerate(path):
        for cheat_target in valid_cheat_targets(node, maze, height, width):
            target_index = path_indices[tuple(cheat_target)]
            time_saved = target_index - start_index - 2
            if time_saved >= 100:
                solution_part_1 += 1

    solution_part_2 = 0
    for p_1, p_2 in itertools.product(path, path):
        if p_1 is p_2:
            continue

        distance = np.sum(np.abs(p_1 - p_2))
        if distance > 20:
            continue

        p_1_index = path_indices[tuple(p_1)]
        p_2_index = path_indices[tuple(p_2)]
        time_saved = p_1_index - p_2_index - distance

        if time_saved >= 100:
            solution_part_2 += 1

    print(solution_part_1)
    print(solution_part_2)


def four_neighbourhood(y, x, height=None, width=None) -> np.ndarray:
    if y < height-1:
        yield np.array([y + 1, x])

    if x < width-1:
        yield np.array([y, x + 1])

    if y > 0:
        yield np.array([y - 1, x])

    if x > 0:
        yield np.array([y, x - 1])


def valid_cheat_targets(origin, maze, height, width) -> np.ndarray:
    if origin[0] < height-2:
        d = np.array([1, 0])
        if maze[*(origin + d)] == "#":
            cheat_target = origin + (2*d)
            if maze[*cheat_target] in [".", "E"]:
                yield cheat_target

    if origin[1] < width-2:
        d = np.array([0, 1])
        if maze[*(origin + d)] == "#":
            cheat_target = origin + (2*d)
            if maze[*cheat_target] in [".", "E"]:
                yield cheat_target

    if origin[0] > 1:
        d = np.array([-1, 0])
        if maze[*(origin + d)] == "#":
            cheat_target = origin + (2*d)
            if maze[*cheat_target] in [".", "E"]:
                yield cheat_target

    if origin[1] > 1:
        d = np.array([0, -1])
        if maze[*(origin + d)] == "#":
            cheat_target = origin + (2*d)
            if maze[*cheat_target] in [".", "E"]:
                yield cheat_target


if __name__ == "__main__":
    solve(Path("input.txt"))