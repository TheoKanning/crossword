from crossword.generate import Generator

def optimize(grid, dictionary):
    print("Starting optimization...")
    print("Finding initial solution...")
    best, best_score = _iterate(grid, dictionary)

    if not best.is_complete():
        print("Could not generate solution!")
        return best, best_score

    print("Solution found, score:", best_score)
    print("\nOptimizing quarter sections...")
    best, best_score = _iterate_sections(2, best, dictionary)

    print("\nOptimizing ninth sections...")
    best, best_score = _iterate_sections(3, best, dictionary)

    print("\nDone optimizing, final score:", best_score)

    return best, best_score

def _iterate_sections(sections, grid, dictionary):
    """
    Cuts the grid into chunks and iterates each separately
    """

    best = grid.copy()
    best_score = 0
    num_chunks = sections**2
    chunk = 1
    size = grid.size

    for i in range(sections):
        for j in range(sections):
            print(f"Optimizing chuck {chunk} of {num_chunks}")
            row_range = ((i*size)//sections, ((i+1)*size)//sections)
            col_range = ((j*size)//sections, ((j+1)*size)//sections)
            grid = _clear_letters(row_range, col_range, best)

            grid, score = _iterate(grid, dictionary)

            if score > best_score:
                best = grid
                best_score = score

            print(f"Score after chunk {chunk}: {best_score}")
            chunk += 1
    return best, best_score

def _iterate(grid, dictionary):
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

        if score > best_score:
            best_score = score
            best = result
        else:
            break

    return best, best_score

def _clear_letters(row_range, col_range, grid):
    """
    Returns a copy of the grid with letters in the given range removed
    Leaves blocks untouched
    row_range: (row_min, row_max)
    col_range: (col_min, col_max)
    """
    output = grid.copy()
    for row in range(*row_range):
        for col in range(*col_range):
            if not grid.is_block((row, col)):
                output.set_square((row, col), '')

    return output
