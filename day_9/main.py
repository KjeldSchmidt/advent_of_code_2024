from pathlib import Path


def solve(path: Path) -> None:
    text = path.read_text().strip()

    abbreviated_blocks = [int(block) for block in text]
    file_blocks = []
    file_ids = []

    for block_idx, block_len in enumerate(abbreviated_blocks):
        if block_idx % 2 == 0:
            file_id = block_idx // 2
            file_blocks.extend([file_id] * block_len)
            file_ids.append(file_id)
        else:
            file_blocks.extend([-1] * block_len)
            file_ids.append(None)

    left_pointer = 0
    right_pointer = len(file_blocks) - 1

    while left_pointer != right_pointer:
        if file_blocks[left_pointer] != -1:
            left_pointer += 1

        elif file_blocks[right_pointer] == -1:
            del file_blocks[right_pointer]
            right_pointer -= 1

        else:
            file_blocks[left_pointer] = file_blocks[right_pointer]
            del file_blocks[right_pointer]
            left_pointer += 1
            right_pointer -= 1

    solution_part_1 = sum([block_idx * file_idx for block_idx, file_idx in enumerate(file_blocks)])
    print(solution_part_1)

    moved_abbreviated_file_blocks = abbreviated_blocks[:]

    file_move_candidate = len(moved_abbreviated_file_blocks) - 1
    while file_move_candidate != 0:
        file_id = file_ids[file_move_candidate]

        if file_id is None or file_id < 0:
            file_move_candidate -= 1
            continue

        for move_index_candidate, length in enumerate(moved_abbreviated_file_blocks):
            if (
                file_ids[move_index_candidate] is None
                and move_index_candidate < file_move_candidate
                and moved_abbreviated_file_blocks[move_index_candidate] >= moved_abbreviated_file_blocks[file_move_candidate]
            ):
                moved_file_length = moved_abbreviated_file_blocks[file_move_candidate]
                moved_abbreviated_file_blocks[move_index_candidate] -= moved_file_length
                moved_abbreviated_file_blocks.insert(move_index_candidate, moved_file_length)
                file_ids[file_ids.index(file_id)] = None
                file_ids.insert(move_index_candidate, -file_id)
                break
        else:
            file_move_candidate -= 1

    file_blocks = []
    for block_idx, block_len in enumerate(moved_abbreviated_file_blocks):
        file_id = file_ids[block_idx]
        if file_id is not None:
            file_blocks.extend([abs(file_id)] * block_len)
        else:
            file_blocks.extend([0] * block_len)

    solution_part_2 = sum([block_idx * file_idx for block_idx, file_idx in enumerate(file_blocks)])

    print(solution_part_2)


if __name__ == "__main__":
    solve(Path("input.txt"))