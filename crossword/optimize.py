from crossword.generate import Generator

def optimize(grid, dictionary, optimize_sections=False):
    print("Starting optimization...")
    print("Finding initial solution...")
    best, best_score = _iterate(grid, dictionary)

    if not best.is_complete():
        print("Could not generate solution!")
        return best, best_score

    best.print()
    print("Solution found, score:", best_score)

    if optimize_sections:
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
    best_score = _grid_score(grid, dictionary)
    num_chunks = sections**2
    chunk = 1
    size = grid.size

    for i in range(sections):
        for j in range(sections):
            print(f"Optimizing chunk {chunk} of {num_chunks}")
            row_range = ((i*size)//sections, ((i+1)*size)//sections)
            col_range = ((j*size)//sections, ((j+1)*size)//sections)
            grid = _clear_letters(row_range, col_range, best)

            grid, score = _iterate(grid, dictionary, best_score)

            if score > best_score:
                best = grid
                best_score = score

            print(f"Score after chunk {chunk}: {best_score}")
            chunk += 1
    return best, best_score

def _iterate(grid, dictionary, target_score=None):
    """
    Repeatedly fills the given grid with a higher target each time
    Can take a known target score to speed up initial searches
    """
    generator = Generator(dictionary)

    best = grid.copy()
    best_score = target_score

    while True:
        result, score = generator.optimize(
              grid,
              target_score=best_score + 1 if best_score else None,
              search_time=10,
              verbose=False)

        print(score)
        if not best_score or score > best_score:
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

def _grid_score(grid, dictionary):
    if not grid.is_complete():
        return None

    score = 0
    for s, m in grid.get_all_words():
        word = grid.get_word(s, m)
        score += int(dictionary.search(word)[0][1])

    return score
