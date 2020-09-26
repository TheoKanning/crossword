import argparse
import sys
import time

from crossword import generate, grid, storage

parser = argparse.ArgumentParser(description='Fill in missing crossword squares,')
parser.add_argument('filename', help='Path to the uncompleted crossword file')
filename = parser.parse_args().filename

grid = grid.Grid(storage.load(filename))
start = time.time()
generator = generate.Generator()

generator.search(grid)

grid.print()
seconds = time.time() - start
nodes = generator.nodes_searched
print(f"Generation took {seconds:.2f} seconds")
print(f"Searched {nodes} nodes, {nodes/seconds:.2f} nodes/sec")
