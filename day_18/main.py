from pathlib import Path
import networkx as nx


def solve(path: Path) -> None:
    text = path.read_text().strip().strip()
    walls = [tuple(map(int, line.split(","))) for line in text.splitlines()]
    part_1_walls = walls[:1024]
    height = 71
    width = 71

    graph = build_graph(height, part_1_walls, width)

    start = (0, 0)
    end = (width-1, height-1)
    solution_part_1 = nx.shortest_path_length(graph, start, end)

    upper_limit = len(walls) - 1
    lower_limit = 0
    while True:
        check_value = lower_limit + (upper_limit-lower_limit)//2
        part_2_walls = walls[:check_value]
        graph = build_graph(height, part_2_walls, width)

        if not nx.has_path(graph, start, end):
            upper_limit = check_value
        else:
            lower_limit = check_value

        if upper_limit == lower_limit + 1:
            break

    solution_part_2 = f"{walls[lower_limit][0]},{walls[lower_limit][1]}"

    print(solution_part_1)
    print(solution_part_2)


def build_graph(height, walls, width):
    graph = nx.Graph()
    for x in range(width):
        for y in range(height):
            if (x, y) in walls:
                continue

            for neighbor in four_neighbourhood(x, y, height, width):
                if neighbor in walls:
                    continue

                graph.add_edge((x, y), neighbor)
    return graph


def four_neighbourhood(x, y, height=None, width=None) -> tuple[int, int]:
    if height is None or y < height-1:
        yield  x, y + 1,

    if width is None or x < width-1:
        yield x + 1, y,

    if height is None or y > 0:
        yield  x, y - 1,

    if width is None or x > 0:
        yield x - 1, y,


if __name__ == "__main__":
    solve(Path("input.txt"))