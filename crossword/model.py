from collections import namedtuple
from copy import deepcopy

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
        assert len(squares) == len(squares[0])
        self.size = len(squares)
        self.squares = deepcopy(squares)
        self.filename = filename
        self.focus = (0, 0)
        self.highlight = []

    def update_focus(self, row, col):
        self.focus = (row, col)
        self.highlight = self.get_highlighted_squares(self.squares, row, col)

    def update_square(self, row, col, text):
        self.squares[row][col] = text
        self.focus = self.get_next_focus(row, col, text)
        self.highlight = self.get_highlighted_squares(self.squares, self.focus[0], self.focus[1])

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

    def get_next_focus(self, row, col, text):
        """
        Get the coordinates of the square that should be focused after the given square
        """
        if text == '':
            # don't move forward if text was deleted
            return (row, col)

        col += 1
        if col >= self.size:
            row += 1
            col = 0
        if row >= self.size:
            row = 0
            col = 0

        if self.squares[row][col] == BLOCK:
            # if the next square is a block, try again starting at the new square
            return self.get_next_focus(row, col, text)

        return (row, col)

