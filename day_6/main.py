import time
from pathlib import Path
import numpy as np
from concurrent.futures import ProcessPoolExecutor, as_completed


def solve(path: Path) -> None:
    text = path.read_text()
    array: np.ndarray = np.array([list(row) for row in text.splitlines()])
    direction = np.array([-1, 0])

    start = time.time()
    walk_entire_path(array, direction)

    print(len(np.argwhere(array == "X")))
    end = time.time()
    print(f"start: {start}, end: {end}, duration: {end - start}")

    start = time.time()
    original_array: np.ndarray = np.array([list(row) for row in text.splitlines()])
    original_guard_position = np.argwhere(original_array == "^")[0].tolist()
    candidates: list[int] = np.argwhere(array == "X").tolist()
    try:
        guard_starting_index = candidates.index(original_guard_position)
        candidates.pop(guard_starting_index)
    except ValueError:
        pass
    candidates_count = len(candidates)

    loops = 0
    with ProcessPoolExecutor() as executor:
        # Map candidates to their processing
        futures = {executor.submit(process_candidate, candidate, original_array): candidate for candidate in candidates}

        finished = 0
        for future in as_completed(futures):
            finished += 1
            print(f"Finished {finished}/{candidates_count}")
            if future.result():
                loops += 1


    end = time.time()
    print(f"start: {start}, end: {end}, duration: {end - start}")
    print(loops)


def process_candidate(candidate, original_array):
    array: np.ndarray = original_array.copy()
    array[tuple(candidate)] = "O"
    direction = np.array([-1, 0])
    walk_terminated = walk_entire_path(array, direction)
    return not walk_terminated  # True if loop is detected


def update_direction(direction: np.ndarray) -> np.ndarray:
    rotation = np.array([
        [0, 1],
        [-1, 0]
    ])

    return np.matmul(rotation, direction)


def walk_entire_path(array: np.ndarray, direction: np.ndarray, max_steps = 10000):
    steps = 0
    while len((guard := np.argwhere(array == "^"))) == 1:
        next_field_index = (guard + direction)[0]

        if not (0 <= next_field_index[0] < array.shape[0]) or not (0 <= next_field_index[1] < array.shape[1]):
            array[*guard[0]] = "X"
            return True

        next_field_value = array[*next_field_index]

        if next_field_value in [".", "X"]:
            array[*guard[0]] = "X"
            array[*next_field_index] = "^"
        elif next_field_value in ["#", "O"]:
            direction = update_direction(direction)
        else:
            print(f"Unexpected value in maze, found {next_field_value}")

        steps += 1
        if steps > max_steps:
            return False


if __name__ == '__main__':
    solve(Path("input.txt"))