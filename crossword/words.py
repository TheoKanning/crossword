from collections import namedtuple

# todo make an enum or something, this looks stupid
BACKGROUND_WHITE = 0
BACKGROUND_BLACK = 1
BACKGROUND_YELLOW = 2

BLOCK='.' # todo move this definition into one place

Square = namedtuple('Square', ['text', 'background', 'focused'])

class Puzzle:
    """
    A class that holds all of the state for a crossword puzzle.
    """
    def __init__(self, squares, filename):
        # todo load crossword by filename here, or default to empty 15x15 array
        # todo store blank squares as empty here, only use spaces when persisting
        assert len(squares) == len(squares[0])
        self.size = len(squares)
        self.squares = squares
        self.filename = filename
        self.focus = (0, 0)
        self.highlight = []

    def update_focus(self, row, col):
        self.focus = (row, col)
        self.highlight = self.get_highlighted_squares(self.squares, row, col)

    def update_square(self, row, col, text):
        self.squares[row][col] = text
        self.highlight = self.get_highlighted_squares(self.squares, row, col)

    def get_square(self, row, col):
        text = self.squares[row][col]
        background = BACKGROUND_WHITE
        if text == BLOCK:
            background = BACKGROUND_BLACK
        elif (row, col) in self.highlight:
            background = BACKGROUND_YELLOW
        focused = (row, col) == self.focus
        return Square(text, background, focused)

    def get_highlighted_squares(self, crossword, row, col):
        """
        Return the coordinates of all of the squares that form a continuous word
        with the given square.
        """
        if self.squares[row][col] == BLOCK:
            return []
        (start, end) = self.get_highlighted_indices(crossword[row], col)
        return [(row, i) for i in range(start, end + 1)]

    def get_word(self, row, col):
        """
        Finds the word containing the given square
        todo use highlights to get this
        """
        row_word = self.squares[row]
        (start, end) = self.get_highlighted_indices(row_word, col)
        return ''.join([char if char != '' else ' ' for char in row_word[start:end + 1]])

    def get_highlighted_indices(self, word, index):
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
        for i in range(index, self.size):
            if word[i] == BLOCK:
                break
            end = i
        return (start, end)

