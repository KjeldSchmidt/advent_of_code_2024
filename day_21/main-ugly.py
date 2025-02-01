from pathlib import Path
from typing import TypeAlias

ClickType: TypeAlias = None
click_action: ClickType = None

d_pad_coords = {
    "A": (0, 2),
    "^": (0, 1),
    "<": (1, 0),
    "v": (1, 1),
    ">": (1, 2),
}

key_coords = {
    "A": (3, 2),
    "0": (3, 1),
    "1": (2, 0),
    "2": (2, 1),
    "3": (2, 2),
    "4": (1, 0),
    "5": (1, 1),
    "6": (1, 2),
    "7": (0, 0),
    "8": (0, 1),
    "9": (0, 2),
}


def solve(path: Path) -> None:
    codes = path.read_text().strip().splitlines()
    solution_part_1 = 0
    solution_part_2 = 0

    for code in codes:
        k_moves = get_d_pad_moves_for_keypad(code)
        d_1_moves = get_d_pad_moves_for_d_pad(k_moves)
        d_2_moves = get_d_pad_moves_for_d_pad(d_1_moves)
        numeric = int(code[:-1])
        sequence_length = len(d_2_moves)
        complexity = numeric * sequence_length
        print(code)
        print(f"{numeric} * {sequence_length} = {complexity}")
        print(d_2_moves)
        print()
        solution_part_1 += complexity

    print(solution_part_1)
    print(solution_part_2)


def get_d_pad_moves_for_keypad(code: str) -> str:
    current_pos = key_coords["A"]

    d_pad_sequence = []
    for button in code:
        next_pos = key_coords[button]
        move = get_move_coords(current_pos, next_pos)

        # if current_pos[0] != 3 and move[1] < 0:
        #     d_pad_sequence.extend(["<"] * abs(move[1]))

        if move[0] < 0:
            d_pad_sequence.extend(["^"] * abs(move[0]))

        if True and move[1] < 0:
            d_pad_sequence.extend(["<"] * abs(move[1]))

        if move[1] > 0:
            d_pad_sequence.extend([">"] * abs(move[1]))

        if move[0] > 0:
            d_pad_sequence.extend(["v"] * abs(move[0]))

        d_pad_sequence.append("A")
        current_pos = next_pos

    return "".join(d_pad_sequence)


def get_d_pad_moves_for_d_pad(code: str) -> str:
    current_pos = d_pad_coords["A"]
    moves = []
    for button in code:
        next_pos = d_pad_coords[button]
        moves.append(get_move_coords(current_pos, next_pos))
        moves.append(click_action)
        current_pos = next_pos

    d_pad_sequence = []
    for move in moves:
        if move == click_action:
            d_pad_sequence.append("A")
            continue

        if move[1] > 0:
            d_pad_sequence.extend([">"] * abs(move[1]))

        if move[0] < 0:
            d_pad_sequence.extend(["^"] * abs(move[0]))

        if move[0] > 0:
            d_pad_sequence.extend(["v"] * abs(move[0]))

        if move[1] < 0:
            d_pad_sequence.extend(["<"] * abs(move[1]))

    return "".join(d_pad_sequence)


def get_move_coords(current: tuple[int, int], target: tuple[int, int]) -> tuple[int, int]:
    return target[0] - current[0], target[1] - current[1]


if __name__ == "__main__":
    solve(Path("input-example.txt"))
    print("Expected: 8, 0, 8, 4, 4")
    # print(get_d_pad_moves_for_d_pad("^A<<^^A>>AvvvA"))
    # print(get_d_pad_moves_for_d_pad("^A^^<<A>>AvvvA"))