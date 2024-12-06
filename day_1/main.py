from pathlib import Path

def solve(path: Path) -> int:
    input = path.read_text()
    list_1 = []
    list_2 = []
    for line in input.split("\n"):
        list_1_entry, list_2_entry = line.split()
        list_1.append(int(list_1_entry))
        list_2.append(int(list_2_entry))

    list_1.sort()
    list_2.sort()
    total_distance = 0
    for pair in zip(list_1, list_2):
        total_distance += abs(pair[0] - pair[1])

    print(total_distance)

    total_similarity = 0
    for number in list_1:
        total_similarity += number * len(list(filter(lambda x: x == number, list_2)))

    print(total_similarity)


solve(Path("input-1.txt"))
