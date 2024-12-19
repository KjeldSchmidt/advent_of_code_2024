from operator import xor
from pathlib import Path
from typing import Callable

outputs = []


def solve_part_1(path: Path) -> None:
    registers, instructions = path.read_text().strip().split("\n\n")

    registers = [int(line.split(":")[1].strip()) for line in registers.splitlines()]
    instructions = [int(instruction) for instruction in instructions.split(":")[1].split(",")]

    run_program(instructions, registers)

    solution = ",".join([str(num) for num in outputs])
    print(solution)


def solve_part_2(path: Path) -> None:
    registers, instructions = path.read_text().strip().split("\n\n")

    instructions = [int(instruction) for instruction in instructions.split(":")[1].split(",")]

    initial_register_a = 8**15
    i = 15
    step_size = 8**i

    while True:
        outputs.clear()
        registers = [initial_register_a, 0, 0]
        run_program(instructions, registers)
        if outputs == instructions:
            break

        if outputs[i] == instructions[i] and i > 0:
            i -= 1
            step_size = 8**i
        else:
            initial_register_a += step_size

    solution = initial_register_a
    print(solution)


def run_program(instructions, registers):
    instruction_ptr = 0
    while instruction_ptr < len(instructions):
        instruction = instructions[instruction_ptr]
        operand = instructions[instruction_ptr + 1]
        operand_value = get_operand_value(operand, instruction, registers)
        instruction_handler = get_instruction_handler(instruction)

        new_instruction_ptr = instruction_handler(registers, operand_value)
        if new_instruction_ptr is None:
            instruction_ptr += 2
        else:
            instruction_ptr = new_instruction_ptr


def get_operand_value(operand: int, instruction: int, registers: list[int] ) -> int:
    if not 0 <= operand < 7:
        assert False, f"Operand {operand} not valid!"

    if instruction in [0, 2, 5, 6, 7]:
        if 0 <= operand <= 3:
            return operand

        return registers[operand - 4]

    return operand


def get_instruction_handler(instruction: int) -> Callable[[list[int], int], None | int]:
    handler_map = {
        0: adv,
        1: bxl,
        2: bst,
        3: jnz,
        4: bxc,
        5: out,
        6: bdv,
        7: cdv,
    }

    return handler_map[instruction]


def adv(registers: list[int], operand: int) -> None:
    registers[0] = registers[0] // (2**operand)


def bxl(registers: list[int], operand: int) -> None:
    registers[1] = xor(registers[1], operand)


def bst(registers: list[int], operand: int) -> None:
    registers[1] = operand % 8


def jnz(registers: list[int], operand: int) -> int | None:
    if registers[0] == 0:
        return None

    return operand


def bxc(registers: list[int], operand: int) -> None:
    registers[1] = xor(registers[1], registers[2])


def out(registers: list[int], operand: int) -> None:
    outputs.append(operand % 8)


def bdv(registers: list[int], operand: int) -> None:
    registers[1] = registers[0] // (2**operand)


def cdv(registers: list[int], operand: int) -> None:
    registers[2] = registers[0] // (2**operand)


if __name__ == "__main__":
    solve_part_1(Path("input.txt"))
    solve_part_2(Path("input.txt"))