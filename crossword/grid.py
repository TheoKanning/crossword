from copy import deepcopy
from enum import Enum

class Mode(Enum):
    ACROSS = 0
    DOWN = 1

BLOCK = '.'

class Grid:
    """
    A class that holds the letters and blocks of a crossword grid.
    """
    def __init__(self, squares=None, size=15):
        if squares:
            assert len(squares) == len(squares[0])
            size = len(squares)
        else:
            squares = [['' for i in range(0,size)] for j in range(0,size)]

        self.squares = deepcopy(squares)
        self.size = size

    def get_square(self, square):
        return self.squares[square[0]][square[1]]

    def set_square(self, square, text):
        assert len(text) <= 1
        self.squares[square[0]][square[1]] = text.upper()

    def get_word(self, square, mode):
        """
        Finds the word containing the given square
        """
        squares = self.get_word_squares(square, mode)
        chars = [self.get_square(s) for s in squares]
        return ''.join([char if char != '' else ' ' for char in chars])

    def get_word_squares(self, square, mode):
        """
        Return the coordinates of all of the squares that form a continuous word
        with the given square.
        """
        row, col = square
        if self.squares[row][col] == BLOCK:
            return []

        word_squares = []
        horizontal = mode is Mode.ACROSS
        index = col if horizontal else row

        for i in range(index, -1, -1):
            square = (row, i) if horizontal else (i, col)
            if self.squares[square[0]][square[1]] == BLOCK:
                break
            word_squares.append(square)

        for i in range(index, self.size):
            square = (row, i) if horizontal else (i, col)
            if self.squares[square[0]][square[1]] == BLOCK:
                break
            word_squares.append(square)

        word_squares = list(set(word_squares))
        word_squares.sort()
        return word_squares

    def print(self):
        for row in self.squares:
            print( ''.join([char if char != '' else ' ' for char in row]))
