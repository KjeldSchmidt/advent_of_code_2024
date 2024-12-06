from collections import defaultdict
from pathlib import Path
import functools

def solve(path: Path) -> None:
    text = path.read_text()
    order, updates = text.split("\n\n")

    preprints: dict[int, list[int]] = defaultdict(list)

    for preprint in order.splitlines():
        source, target = preprint.split("|")
        preprints[int(source)].append(int(target))

    sum = 0
    disordered_pages = []
    for update in updates.splitlines():
        pages = [int(page) for page in update.split(",")]

        pages = list(reversed(pages))
        is_out_of_order = False
        for page_idx, page in enumerate(pages):
            for preceding_page in pages[page_idx+1:]:
                if preceding_page in preprints[page]:
                    is_out_of_order = True

        if not is_out_of_order:
            sum += pages[len(pages) // 2]
        else:
            disordered_pages.append(pages)

    print(sum)

    # Part 2

    def compare_pages(value, other):
        if value in preprints[other]:
            return 1
        if other in preprints[value]:
            return -1
        return 0

    example = disordered_pages[-14]
    print(example)
    for page in example:
        print(f"{page}: {sorted(preprints[page])}")
    print(sorted(example, key=functools.cmp_to_key(compare_pages)))

    sum = 0
    for pages in disordered_pages:
        sorted_pages = sorted(pages, key=functools.cmp_to_key(compare_pages))
        print(pages)
        print(sorted_pages)
        print()
        print()
        sum += sorted_pages[len(pages) // 2]

    print(sum)





solve(Path("input.txt"))
