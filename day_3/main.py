import re
from pathlib import Path

def solve_part_1(path: Path):
    text = path.read_text()
    matches = re.findall("mul\(\d+,\d+\)", text)
    sum = 0
    for match in matches:
        sum += eval(match)

    print(sum)

def solve_part_2(path: Path):
    text = path.read_text()
    enabled = True
    sum = 0

    while len(text) > 0:
        next_enable = re.search("do\(\)", text)
        next_disable = re.search("don't\(\)", text)
        next_mul = re.search("mul\(\d+,\d+\)", text)

        next_enable_start = 10e10 if next_enable is None else next_enable.start()
        next_disable_start = 10e10 if next_disable is None else next_disable.start()
        next_mul_start = 10e10 if next_mul is None else next_mul.start()

        if next_enable is None and next_disable is None and next_mul is None:
            break

        if next_enable_start < min(next_disable_start, next_mul_start):
            enabled = True
            print("enabled = True")
            text = text[next_enable.end():]

        if next_disable_start < min(next_enable_start, next_mul_start):
            enabled = False
            print("enabled = False")
            text = text[next_disable.end():]

        if next_mul_start < min(next_enable_start, next_disable_start):
            if enabled:
                expression = text[next_mul.start():next_mul.end()]
                print(f"{expression=}")
                value = eval(expression)
                print(f"{expression} = {value}")
                sum += value
                print(f"done with sum += {expression}")
            text = text[next_mul.end():]

        print()

    print(sum)


def mul(a, b):
    return a * b

solve_part_1(Path("input.txt"))
solve_part_2(Path("input.txt"))