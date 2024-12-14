from dataclasses import dataclass
from pathlib import Path
import re
import numpy as np


@dataclass
class Machine:
    A: tuple[int, int]
    B: tuple[int, int]
    P: tuple[int, int]


def solve(path: Path) -> None:
    text = path.read_text()
    machines_desc = text.strip().split("\n\n")

    solution_part_1 = 0
    solution_part_2 = 0

    for machine_desc in machines_desc:
        x_values = re.findall(r"X[\+=](\d+)", machine_desc)
        y_values = re.findall(r"Y[\+=](\d+)", machine_desc)
        machine = Machine(*zip(x_values, y_values))

        A = np.array([machine.A, machine.B], dtype=int).T
        b = np.array(machine.P, dtype=int)
        b_2 = b + np.array([10000000000000, 10000000000000])
        x = np.linalg.solve(A, b)
        x_2 = np.linalg.solve(A, b_2)

        if np.allclose(x, np.round(x)):
            x = np.round(x)
            tokens = int(3 * x[0] + x[1])
            solution_part_1 += tokens

        if np.allclose(x_2, np.round(x_2), rtol=0, atol=1e-1):
            x_2 = np.round(x_2)
            tokens = int(3 * x_2[0] + x_2[1])
            solution_part_2 += tokens


    print(solution_part_1)
    print(solution_part_2)


if __name__ == "__main__":
    solve(Path("input.txt"))