import math
from pathlib import Path

def solve(path: Path):
    text = path.read_text()
    reports = [list(map(int, report.split())) for report in text.split("\n")]

    print(len(list(filter(lambda x: x, map(is_report_safe, reports)))))

    print(len(list(filter(lambda x: x, map(is_report_safe_when_dampened, reports)))))


def is_report_safe_when_dampened(report: list[int]) -> bool:
    dampened_safeties = []
    for i in range(len(report)):
        dampened_report = [datum for datum in report]
        del dampened_report[i]
        dampened_safeties.append(is_report_safe(dampened_report))

    return any(dampened_safeties)


def is_report_safe(report: list[int]) -> bool:
    expected_sign = None
    for i in range(len(report) - 1):
        difference = report[i] - report[i+1]
        if expected_sign is None:
            expected_sign = sign(difference)
        elif sign(difference) != expected_sign:
            return False

        if not 1 <= abs(difference) <= 3:
            return False

    return True


def sign(number) -> int:
    return math.copysign(1, number)



solve(Path("input.txt"))
