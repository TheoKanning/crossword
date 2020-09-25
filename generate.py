import time
from crossword import generate, grid

squares = [
        ['.','M', 'A', 'A', 'M'],
        [ '', '', '', '', ''],
        [ '', '', '', '', ''],
        [ '', '', '', '', ''],
        [ 'B', 'O', 'R', 'B', '.'],
        ]


if __name__ == '__main__':
    grid = grid.Grid(squares)
    start = time.time()
    generator = generate.Generator()
    generator.search(grid)
    grid.print()
    seconds = time.time() - start
    nodes = generator.nodes_searched
    print(f"Generation took {seconds:.2f} seconds")
    print(f"Searched {nodes} nodes, {nodes/seconds:.2f} nodes/sec")
