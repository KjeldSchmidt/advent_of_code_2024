import functools
import time
from pathlib import Path


def solve(path: Path) -> None:
    text = path.read_text()
    # text = "0 1 2"


    stones = [int(stone) for stone in text.split()]
    solution_part_1 = 0
    for stone in stones:
        solution_part_1 += stone_count_after_iterations(stone, 25)

    solution_part_2 = 0
    start = time.time()
    for stone in stones:
        solution_part_2 += stone_count_after_iterations(stone, 75)
    end = time.time()

    print()
    print(f"{solution_part_1=}")
    print(f"{solution_part_2=}")

    print(f"Part 2 took {(end - start):2f}s")



def blink(stones: list[int]):
    new_stones = []
    for stone in stones:
        new_stones.extend(split_stone(stone))
    return new_stones


@functools.cache
def stone_count_after_iterations(stone, iterations):
    if iterations == 0:
        return 1

    new_stones = split_stone(stone)
    result = 0
    for new_stone in new_stones:
        partial_result = stone_count_after_iterations(new_stone, iterations - 1)
        result += partial_result

    return result


@functools.cache
def split_stone(stone: int) -> list[int]:
    new_stones = []
    if stone == 0:
        new_stones.append(1)
    elif len(str(stone)) % 2 == 0:
        stone = str(stone)
        left_stone = int(stone[:len(stone) // 2])
        right_stone = int(stone[len(stone) // 2:])
        new_stones.append(left_stone)
        new_stones.append(right_stone)
    else:
        new_stones.append(stone*2024)
    return new_stones



if __name__ == "__main__":
    solve(Path("input.txt"))