from crossword.generate import Generator

def optimize(grid, dictionary):
    best, best_score = iterate(grid, dictionary)
    return best, best_score

def iterate(grid, dictionary):
    """
    Repeatedly fills the given grid with a higher target each time
    """
    generator = Generator(dictionary)

    best, best_score = generator.optimize(
        grid,
        target_score=None,
        search_time=3,
        verbose=False)

    while True:
        result, score = generator.optimize(
              grid,
              target_score=best_score + 1,
              search_time=3,
              verbose=False)

        print("Finished with score", score)

        if score > best_score:
            best_score = score
            best = result
        else:
            break

    return best, best_score

def _clear_letters(x_range, y_range, grid):
    """
    Returns a copy of the grid with letters in the given range removed
    Leaves blocks untouched
    """
    
