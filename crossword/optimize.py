from crossword.generate import Generator

def optimize(grid, dictionary):

    generator = Generator(dictionary)
    best, best_score = generator.optimize(grid, target_score=None, verbose=False)

    return best, best_score
