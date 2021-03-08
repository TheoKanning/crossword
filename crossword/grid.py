from copy import deepcopy
from enum import Enum


class Mode(Enum):
    ACROSS = 0
    DOWN = 1

    def opposite(self):
        return Mode.ACROSS if self == Mode.DOWN else Mode.DOWN


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
            squares = [['' for i in range(0, size)] for j in range(0, size)]

        self.squares = deepcopy(squares)
        self.size = size

    def copy(self):
        return Grid(self.squares)

    def get_square(self, square):
        return self.squares[square[0]][square[1]]

    def is_empty(self, square):
        return self.get_square(square) == ''

    def is_block(self, square):
        return self.get_square(square) == BLOCK

    def is_complete(self):
        for row in self.squares:
            for letter in row:
                if letter == '':
                    return False
        return True

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

    def get_all_words(self):
        """
        Traverses the whole grid and returns a list containing the direction and start of each word.
        """
        words = []

        for row in range(self.size):
            for col in range(self.size):
                if self.is_block((row, col)):
                    continue

                if col == 0 or self.is_block((row, col - 1)):
                    words.append(((row, col), Mode.ACROSS))

                if row == 0 or self.is_block((row - 1, col)):
                    words.append(((row, col), Mode.DOWN))

        return words

    def print(self):
        for row in self.squares:
            print(''.join([char if char != '' else ' ' for char in row]))
