from copy import deepcopy
from crossword import dictionary
from crossword.grid import Grid, Mode

nodes_searched = 0

    # todo generate these one at a time in case not all of them are needed?
    # todo end early if no words are left
def get_possible_words(grid, square, mode):
    """ Returns a list of all possible words for a given square and direction
        sorted from best to worst
    """
    word = grid.get_word(square, mode)
    words = [w[0] for w in dictionary.search(word)] # strip point value
    cross_mode = mode.opposite()
    updated_squares = grid.get_word_squares(square, mode)

    # remove any words that would cause a contradiction later
    for i, s in enumerate(updated_squares):
        if not grid.is_empty(s):
            continue # skip squares that are already filled in

        cross_index = grid.get_word_squares(s, cross_mode).index(s)
        cross_word = grid.get_word(s, cross_mode)
        letters = dictionary.get_allowed_letters(cross_word, cross_index)
        words = [w for w in words if w[i] in letters]

    return words

def get_next_target(grid, previous_direction):
    """ Returns the next square and direction to search.
    todo this needs to enforce a consistent order, or backtracking won't work as effectively
    ideally this should finish a corner of the puzzle before moving on to other areas
    """
    direction = Mode.DOWN if previous_direction == Mode.ACROSS else Mode.ACROSS
    for i in range(grid.size):
        for j in range(grid.size):
            if grid.is_empty((i, j)):
                return ((i, j), direction)

    return None, None

def set_word(grid, square, mode, word):
    """Fills the given square with the given word
    todo see if it's possible to only use squares that are the start of a clue
    """
    word = word.upper()
    opposite_mode = Mode.DOWN if mode == Mode.ACROSS else Mode.ACROSS
    squares = grid.get_word_squares(square, mode)
    for i, square in enumerate(squares):
        if grid.get_square(square) != word[i]:
            grid.set_square(square, word[i])

def search(grid, previous_mode=Mode.ACROSS):
    """ Recursive function that picks a square then loops through all available words.
    Returns false if no words are valid, true if the puzzle is complete"
    """
    global nodes_searched
    nodes_searched += 1
    if nodes_searched % 100 == 0:
        print(f"{nodes_searched} nodes searched")
        grid.print()
        print("")

    original_squares = deepcopy(grid.squares)
    square, mode = get_next_target(grid, previous_mode)
    if square == None:
        return True # no more words to search
    for word in get_possible_words(grid, square, mode):
        grid.squares = deepcopy(original_squares) #todo this will be slow
        result = set_word(grid, square, mode, word)
        if result == False:
            # word caused a contradiction, keep going to next word
            continue
        result = search(grid, mode)
        if result == True:
            return True

    return False

