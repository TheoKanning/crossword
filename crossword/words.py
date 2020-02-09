BLOCK='.' # todo move this definition into one place

def get_highlighted_squares(crossword, row, col):
    """
    Return the coordinates of all of the squares that form a continuous word
    with the given square.
    """
    (start, end) = get_highlighted_indices(crossword[row], col)
    return [(row, i) for i in range(start, end + 1)]

def get_word(crossword, row, col):
    """
    Finds the word containing the given square
    """
    row_word = crossword[row]
    (start, end) = get_highlighted_indices(row_word, col)
    return ''.join(row_word[start:end + 1])

def get_highlighted_indices(word, index):
    """
    Return the 1-D start and end points of the word containing the given index
    Starts at given index and counts down/up until a block is found.
    """
    start = index
    for i in range(index, -1, -1):
        if word[i] == BLOCK:
            break
        start = i
    end = index
    for i in range(index, 15):
        if word[i] == BLOCK:
            break
        end = i
    return (start, end)

