from pathlib import Path


def solve(path: Path) -> None:
    text = path.read_text()


    task_1_sum = 0
    task_2_sum = 0
    for line in text.splitlines():
        test_value, numbers = line.split(':')
        test_value = int(test_value)
        numbers = [int(num) for num in numbers.split()]
        if can_get_result_with_plus_and_times(test_value, numbers):
            task_1_sum += test_value

        if can_get_result_with_plus_times_and_concatenation(test_value, numbers):
            task_2_sum += test_value

    print(task_1_sum)
    print(task_2_sum)


def can_get_result_with_plus_and_times(result, numbers):
    if len(numbers) == 2:
        if result == numbers[0] + numbers[1]:
            return True

        if result == numbers[0] * numbers[1]:
            return True

        return False

    sum_path = [numbers[0] + numbers[1]] + numbers[2:]
    mul_path = [numbers[0] * numbers[1]] + numbers[2:]

    if can_get_result_with_plus_and_times(result, sum_path):
        return True

    if can_get_result_with_plus_and_times(result, mul_path):
        return True

    return False


def can_get_result_with_plus_times_and_concatenation(result, numbers):
    if len(numbers) == 2:
        if result == numbers[0] + numbers[1]:
            return True

        if result == numbers[0] * numbers[1]:
            return True

        if result == concat_numbers(numbers[0], numbers[1]):
            return True

        return False

    sum_path = [numbers[0] + numbers[1]] + numbers[2:]
    mul_path = [numbers[0] * numbers[1]] + numbers[2:]
    concat_path = [concat_numbers(numbers[0], numbers[1])] + numbers[2:]

    if can_get_result_with_plus_times_and_concatenation(result, sum_path):
        return True

    if can_get_result_with_plus_times_and_concatenation(result, mul_path):
        return True

    if can_get_result_with_plus_times_and_concatenation(result, concat_path):
        return True

    return False


def concat_numbers(a:int, b: int) -> int:
    return int(f"{a}" + f"{b}")



solve(Path("input.txt"))