from pathlib import Path
from typing import TypeAlias

ClickType: TypeAlias = None
click_action: ClickType = None

MoveList: TypeAlias = list[tuple[int, int] | ClickType]

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
        move_count = get_move_count_for_keypad(code)
        code_num = int(code[:-1])
        complexity = move_count * code_num
        solution_part_1 += complexity
        print()
        print(f"Got {code} as {complexity=} with {move_count=} and {code_num=}")

    print(solution_part_1)
    print(solution_part_2)


def get_move_count_for_keypad(code: str) -> int:
    current_pos = key_coords["A"]
    count = 0
    for button in code:
        moves = []
        next_pos = key_coords[button]
        moves.append(get_move_coords(current_pos, next_pos))
        moves.append(click_action)
        current_pos = next_pos
        count += get_move_count_for_top_d_pad(moves)

    return count


def get_move_count_for_top_d_pad(target_moves: MoveList) -> int:
    current_pos = d_pad_coords["A"]
    count = 0
    for move in target_moves:
        moves = []
        if move is click_action:
            next_pos = d_pad_coords["A"]
            moves.append(get_move_coords(current_pos, next_pos))
            moves.append(click_action)
            current_pos = next_pos
            count += get_move_count_for_lower_d_pad(moves)

        else:
            if move[0] < 0:
                next_pos = d_pad_coords["^"]
                moves.append(get_move_coords(current_pos, next_pos))
                moves.extend([click_action] * abs(move[0]))
                current_pos = next_pos
                count += get_move_count_for_lower_d_pad(moves)

            if move[1] < 0:
                next_pos = d_pad_coords["<"]
                moves.append(get_move_coords(current_pos, next_pos))
                moves.extend([click_action] * abs(move[1]))
                current_pos = next_pos
                count += get_move_count_for_lower_d_pad(moves)

            if move[1] > 0:
                next_pos = d_pad_coords[">"]
                moves.append(get_move_coords(current_pos, next_pos))
                moves.extend([click_action] * abs(move[1]))
                current_pos = next_pos
                count += get_move_count_for_lower_d_pad(moves)

            if move[0] > 0:
                next_pos = d_pad_coords["v"]
                moves.append(get_move_coords(current_pos, next_pos))
                moves.extend([click_action] * abs(move[0]))
                current_pos = next_pos
                count += get_move_count_for_lower_d_pad(moves)

    return count


def get_move_count_for_lower_d_pad(target_moves: MoveList, remaining_layers: int = 0) -> int:
    current_pos = d_pad_coords["A"]
    count = 0
    total_moves = []
    for move in target_moves:
        moves = []
        if move is click_action:
            next_pos = d_pad_coords["A"]
            moves.append(get_move_coords(current_pos, next_pos))
            moves.append(click_action)
            current_pos = next_pos
            print("A", end="")

        else:
            if move[1] > 0:
                next_pos = d_pad_coords[">"]
                moves.append(get_move_coords(current_pos, next_pos))
                moves.extend([click_action] * abs(move[1]))
                current_pos = next_pos
                if remaining_layers == 0:
                    print(">" * abs(move[1]), end="")

            if move[0] < 0:
                next_pos = d_pad_coords["^"]
                moves.append(get_move_coords(current_pos, next_pos))
                moves.extend([click_action] * abs(move[0]))
                current_pos = next_pos
                if remaining_layers == 0:
                    print("^" * abs(move[1]), end="")

            if move[0] >     0:
                next_pos = d_pad_coords["v"]
                moves.append(get_move_coords(current_pos, next_pos))
                moves.extend([click_action] * abs(move[0]))
                current_pos = next_pos
                if remaining_layers == 0:
                    print("v" * abs(move[0]), end="")

            if move[1] < 0:
                next_pos = d_pad_coords["<"]
                moves.append(get_move_coords(current_pos, next_pos))
                moves.extend([click_action] * abs(move[1]))
                current_pos = next_pos
                if remaining_layers == 0:
                    print("<" * abs(move[1]), end="")

        if remaining_layers == 0:
            for inner_move in moves:
                if inner_move == click_action:
                    count += 1
                else:
                    count += abs(inner_move[0])
                    count += abs(inner_move[1])

        else:
            count += get_move_count_for_lower_d_pad(moves, remaining_layers=remaining_layers-1)

    return count


def get_move_coords(current: tuple[int, int], target: tuple[int, int]) -> tuple[int, int]:
    return target[0] - current[0], target[1] - current[1]


if __name__ == "__main__":
    solve(Path("input-example.txt"))