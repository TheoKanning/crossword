import argparse
import time

from crossword import dictionary, generate, grid, storage

parser = argparse.ArgumentParser(description='Fill in missing crossword squares,')
parser.add_argument('filename', help='Path to the uncompleted crossword file')
filename = parser.parse_args().filename

dictionary = dictionary.CrosswordDictionary(seed=0)
grid = grid.Grid(storage.load(filename))
start = time.time()
generator = generate.Generator(dictionary)

generator.optimize(grid)

grid.print()
print(f"Total score: {generator.score}")
for s, m in grid.get_all_words():
    word = grid.get_word(s, m)
    score = int(dictionary.search(word)[0][1])
    print(f"{s} {m} {word}: {score}")
seconds = time.time() - start
nodes = generator.nodes_searched

print(f"Generation took {seconds:.2f} seconds")
print(f"Searched {nodes} nodes, {nodes / seconds:.2f} nodes/sec")
