import argparse
import time

from crossword import dictionary, generate, grid, optimize, storage

parser = argparse.ArgumentParser(description='Fill in missing crossword squares,')
parser.add_argument('filename', help='Path to the uncompleted crossword file')
filename = parser.parse_args().filename

dictionary = dictionary.Dictionary(seed=0)
grid = grid.Grid(storage.load(filename))
start = time.time()
generator = generate.Generator(dictionary)

target_score = None
#grid, score = generator.optimize(grid, target_score)
grid, total_score = optimize.optimize(grid, dictionary)

grid.print()
for s, m in grid.get_all_words():
    word = grid.get_word(s, m)
    score = int(dictionary.search(word)[0][1])
    print(f"{s} {m} {word}: {score}")
seconds = time.time() - start
nodes = 0 #generator.nodes_searched

print(f"Total score: {total_score}")
print(f"Generation took {seconds:.2f} seconds")
print(f"Searched {nodes} nodes, {nodes / seconds:.2f} nodes/sec")
