from collections import defaultdict
from functools import cache
from operator import xor
from pathlib import Path


def solve(path: Path) -> None:
    text = path.read_text().strip()
    secrets = [int(line) for line in text.splitlines()]
    solution_part_1 = 0
    solution_part_2 = 0

    sequence_prices: dict[tuple[int, int, int, int], list[int]] = defaultdict(list)

    for secret in secrets:
        seen_sequences: set[tuple[int, int, int, int]] = set()
        price_changes = []
        current_secret = secret
        for _ in range(2000):
            new_secret = evolve_secret_number(current_secret)

            price_changes.append(new_secret % 10 - current_secret % 10)
            sequence = tuple(price_changes)
            if len(price_changes) == 4:
                if sequence not in seen_sequences:
                    sequence_prices[sequence].append(new_secret % 10)
                    seen_sequences.add(sequence)
                del price_changes[0]

            current_secret = new_secret

        solution_part_1 += current_secret

    print(sequence_prices[(-2, 1, -1, 3)])
    for sequence, prices in sequence_prices.items():
        total_for_sequence = sum(prices)
        if total_for_sequence > solution_part_2:
            solution_part_2 = total_for_sequence

    print(solution_part_1)
    print(solution_part_2)


# @cache
def evolve_secret_number(current_secret: int) -> int:
    next_secret = xor(current_secret * 64, current_secret) % 16777216
    next_secret = xor(next_secret // 32, next_secret) % 16777216
    next_secret = xor(next_secret * 2048, next_secret) % 16777216

    return next_secret


if __name__ == "__main__":
    solve(Path("input.txt"))