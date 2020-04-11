from collections import namedtuple
from copy import deepcopy
from enum import Enum

class Mode(Enum):
    HORIZONTAL = 0
    VERTICAL = 1

class Background(Enum):
    WHITE = 0
    BLACK = 1
    YELLOW = 2

BLOCK='.' # todo move this definition into one place

Square = namedtuple('Square', ['text', 'background', 'focused'])

class Puzzle:
    """
    A class that holds all of the state for a crossword puzzle.
    """
    def __init__(self, squares, filename=None):
        # todo load crossword by filename here, or default to empty 15x15 array
        assert len(squares) == len(squares[0])
        self.size = len(squares)
        self.squares = deepcopy(squares)
        self.filename = filename
        self.focus = (0, 0)
        self.highlight = []
        self.mode = Mode.HORIZONTAL

    def toggle_orientation(self):
        self.mode = Mode.VERTICAL if self.mode is Mode.HORIZONTAL else Mode.HORIZONTAL
        self.highlight = self.get_highlighted_squares(self.focus[0], self.focus[1])

    def update_focus(self, row, col):
        self.focus = (row, col)
        self.highlight = self.get_highlighted_squares(row, col)

    def update_square(self, row, col, text):
        if text == BLOCK:
            self.squares[self.size - 1 - row][self.size - 1 - col] = BLOCK
        elif self.squares[row][col] == BLOCK and text != BLOCK:
            self.squares[self.size - 1 - row][self.size - 1 - col] = ''
        self.squares[row][col] = text
        self.focus = self.get_next_focus(row, col, text)
        self.highlight = self.get_highlighted_squares(self.focus[0], self.focus[1])

    def get_square(self, row, col):
        text = self.squares[row][col]
        background = Background.WHITE
        if text == BLOCK:
            background = Background.BLACK
        elif (row, col) in self.highlight:
            background = Background.YELLOW
        focused = (row, col) == self.focus
        return Square(text, background, focused)

    def get_word(self, row, col):
        """
        Finds the word containing the given square
        """
        squares = self.get_highlighted_squares(row, col)
        chars = [self.squares[square[0]][square[1]] for square in squares]
        return ''.join([char if char != '' else ' ' for char in chars])

    def get_highlighted_squares(self, row, col):
        """
        Return the coordinates of all of the squares that form a continuous word
        with the given square.
        """
        if self.squares[row][col] == BLOCK:
            return []

        highlighted = []
        horizontal = self.mode is Mode.HORIZONTAL
        index = col if horizontal else row

        for i in range(index, -1, -1):
            square = (row, i) if horizontal else (i, col)
            if self.squares[square[0]][square[1]] == BLOCK:
                break
            highlighted.append(square)

        for i in range(index, self.size):
            square = (row, i) if horizontal else (i, col)
            if self.squares[square[0]][square[1]] == BLOCK:
                break
            highlighted.append(square)

        highlighted = list(set(highlighted))
        highlighted.sort()
        return highlighted

    def get_next_focus(self, row, col, text):
        """
        Get the coordinates of the square that should be focused after the given square
        """
        if text == '':
            # don't move forward if text was deleted
            return (row, col)

        if self.mode is Mode.HORIZONTAL:
            col += 1
            if col >= self.size:
                row += 1
                col = 0
            if row >= self.size:
                row = 0
                col = 0
        else:
            row += 1
            if row >= self.size:
                row = 0
                col += 1
            if col >= self.size:
                row = 0
                col = 0

        if self.squares[row][col] == BLOCK:
            # if the next square is a block, try again starting at the new square
            return self.get_next_focus(row, col, text)

        return (row, col)

