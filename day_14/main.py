from pathlib import Path

width = 101
height = 103
steps=100


def solve(path: Path) -> None:
    text = path.read_text().strip().splitlines()
    solution_part_2 = 0

    robots_before = []
    robots = []
    for line in text:
        p_t, v_t = line.split()
        p = tuple(map(int, p_t.split('=')[1].split(',')))
        v = tuple(map(int, v_t.split('=')[1].split(',')))

        robots_before.append((p, v))
        position_after = (p[0] + steps*v[0]) % width, (p[1] + steps*v[1]) % height
        robots.append(position_after)

    i = 0
    candidates_h = (538 + i*103 for i in range(100))
    candidates_v = (452 + i*101 for i in range(100))
    candidates = sorted([c for c in candidates_h] + [c for c in candidates_v])
    c_i = 0
    while True:
        positions_now = []
        for p, v in robots_before:
            positions_now.append( ((p[0] + i*v[0]) % width, (p[1] + i*v[1]) % height) )
        show_board(positions_now)
        print(f"Above is iteration {i}")
        command = input("Waiting")
        if command == "b":
            i -= 1
        elif command == "":
            i = candidates[c_i]
            print(f"{c_i}")
            c_i += 1
        else:
            i = int(command)
        print("\033[H\033[J", end="")

    # show_board(robots_before)
    # print()
    # show_board(robots)

    a = b = c = d = 0
    for robot in robots:
        if robot[0] < width//2 and robot[1] < height//2:
            a += 1
        if robot[0] > width//2 and robot[1] < height//2:
            b += 1
        if robot[0] < width//2 and robot[1] > height//2:
            c += 1
        if robot[0] > width//2 and robot[1] > height//2:
            d += 1

    print()
    print(a, b, c, d)
    solution_part_1 = a*b*c*d

    print(solution_part_1)
    print(solution_part_2)


def show_board(robots: list[tuple[int, int]]):
    for y in range(height):
        for x in range(width):
            count = robots.count((x, y))
            display = " " if count == 0 else count
            print(display, end="")
        print()


if __name__ == "__main__":
    solve(Path("input.txt"))