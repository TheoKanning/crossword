from collections import namedtuple

# todo make an enum or something, this looks stupid
BACKGROUND_WHITE = 0
BACKGROUND_BLOCK = 1
BACKGROUND_YELLOW = 2

BLOCK='.' # todo move this definition into one place

Square = namedtuple('Square', ['text', 'background', 'focused'])

class Puzzle:
    """
    A class that holds all of the state for a crossword puzzle.
    """
    def __init__(self, squares, filename):
        assert len(squares) == len(squares[0])
        self.size = len(squares)
        self.squares = squares
        self.filename = filename
        self.focus = (0, 0)
        self.highlight = []

    def update_focus(self, row, col):
        self.focus = (rox, col)
        self.highlight = get_highlighted_squares(self,squares, row, col)

    def update_square(self, row, col, text):
        self.squares[row,col] = text

    def get_square(self, row, col):
        text = self.squares[row][col]
        background = BACKGROUND_WHITE
        if text is BLOCK:
            background = BACKGROUND_BLOCK
        elif (row, col) in self.highlight:
            background = BACKGROUND_YELLOW
        focused = (row, col) is self.focus
        return Square(text, background, focused)

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

