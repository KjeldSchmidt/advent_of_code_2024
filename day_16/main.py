from enum import Enum, auto
from pathlib import Path
import networkx as nx


class D(Enum):
    N = auto()
    E = auto()
    S = auto()
    W = auto()


def solve(path: Path) -> None:
    text = path.read_text().strip()
    maze: list[list[str]] = [[block for block in line] for line in text.splitlines()]
    height = len(maze)
    width = len(maze[0])
    start = (0, 0)
    end = (0, 0)
    graph = nx.Graph()
    for y in range(height):
        for x in range(width):
            block = maze[y][x]

            if block == "#":
                continue

            if block == "E":
                end = (y, x)
            if block == "S":
                start = (y, x, D.E)

            graph.add_edge((y, x, D.E), (y, x, D.N), weight=1000)
            graph.add_edge((y, x, D.E), (y, x, D.S), weight=1000)
            graph.add_edge((y, x, D.W), (y, x, D.N), weight=1000)
            graph.add_edge((y, x, D.W), (y, x, D.S), weight=1000)

            for y_n, x_n, d in four_neighbourhood(y, x, height, width):
                if maze[y_n][x_n] == "#":
                    continue

                graph.add_edge((y, x, d), (y_n, x_n, d), weight=1)

    candidates = {
        D.N: nx.shortest_path_length(graph, start, (end[0], end[1], D.N), weight="weight"),
        D.E: nx.shortest_path_length(graph, start, (end[0], end[1], D.E), weight="weight"),
        D.S: nx.shortest_path_length(graph, start, (end[0], end[1], D.S), weight="weight"),
        D.W: nx.shortest_path_length(graph, start, (end[0], end[1], D.W), weight="weight"),
    }

    solution_part_1 = min(candidates.values())

    nodes_along_shortest_path = set()
    for end_direction, path_length in candidates.items():
        if path_length != solution_part_1:
            continue

        i = 0
        for path in nx.all_shortest_paths(graph, start, (end[0], end[1], end_direction), weight="weight"):
            for node in path:
                nodes_along_shortest_path.add((node[0], node[1]))

            i += 1
            if i == 1000:
                break

    solution_part_2 = len(nodes_along_shortest_path)

    print(f"{solution_part_1=}")
    print(f"{solution_part_2=}")


def show_nodes_in_maze(maze, nodes):
    for y, line in enumerate(maze):
        for x, char in enumerate(line):
            char_to_print = "."
            if char == "#":
                char_to_print = "#"
            if (y, x) in nodes:
                char_to_print = "O"

            print(char_to_print, end="")

        print()


def four_neighbourhood(row, col, height=None, width=None):
    if height is None or row < height-1:
        yield row+1, col, D.S

    if width is None or col < width-1:
        yield row, col+1, D.E

    if height is None or row > 0:
        yield row-1, col, D.N

    if width is None or col > 0:
        yield row, col-1, D.W


if __name__ == "__main__":
    solve(Path("input.txt"))