from pathlib import Path
import networkx as nx


def solve(path: Path) -> None:
    text = path.read_text().strip()
    connections = [line.split("-") for line in text.splitlines()]
    graph = nx.Graph()

    for computer1, computer2 in connections:
        graph.add_edge(computer1, computer2)

    solution_part_1 = 0
    cycles = nx.simple_cycles(graph, length_bound=3)
    for a, b, c in cycles:
        if a[0] == "t" or b[0] == "t" or c[0] == "t":
            solution_part_1 += 1

    lan_party_computers, _ = nx.clique.max_weight_clique(graph, weight=None)
    solution_part_2 = ",".join(sorted(lan_party_computers))

    print(solution_part_1)
    print(solution_part_2)


if __name__ == "__main__":
    solve(Path("input.txt"))