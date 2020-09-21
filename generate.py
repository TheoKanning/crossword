import time
from crossword import search, grid

squares = [
        ['A','M', 'A', 'A', 'M'],
        [ '', '', '', '', ''],
        [ '', '', '', '', ''],
        [ '', '', '', '', ''],
        [ '', '', '', '', ''],
        ]


if __name__ == '__main__':
    grid = grid.Grid(squares)
    start = time.time()
    search.search(grid)
    grid.print()
    seconds = time.time() - start
    nodes = search.nodes_searched
    print(f"Search took {seconds:.2f} seconds")
    print(f"Searched {nodes} nodes, {nodes/seconds:.2f} nodes/sec")
