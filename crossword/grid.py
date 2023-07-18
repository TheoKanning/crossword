import json
from copy import deepcopy
from enum import Enum


class Mode(Enum):
    ACROSS = 0
    DOWN = 1

    def opposite(self):
        return Mode.ACROSS if self == Mode.DOWN else Mode.DOWN


BLOCK = "."


def load_grid(filename):
    with open(filename, "r") as f:
        data = json.load(f)
        return Grid(data["squares"], data["size"], data["clues"])


class Grid:
    """
    A class that holds the blocks, letters, and clues of a crossword grid.
    Everything that needs to be saved between sessions belongs here
    """

    def __init__(self, squares=None, size=15, clues=None):
        if squares:
            assert len(squares) == len(squares[0])
            size = len(squares)
        else:
            squares = [["" for i in range(0, size)] for j in range(0, size)]

        self.squares = deepcopy(squares)
        self.size = size
        self.clues = (
            deepcopy(clues) if clues else {str(Mode.ACROSS): {}, str(Mode.DOWN): {}}
        )  # {mode: {square: clue}}

    def copy(self):
        return Grid(self.squares)

    def get_square(self, square):
        return self.squares[square[0]][square[1]]

    def is_empty(self, square):
        return self.get_square(square) == ""

    def is_block(self, square):
        return self.get_square(square) == BLOCK

    def is_complete(self):
        for row in self.squares:
            for letter in row:
                if letter == "":
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
        return "".join([char if char != "" else " " for char in chars])

    def get_word_squares(self, square, mode):
        """
        Return the coordinates of all the squares that form a continuous word
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

    def get_word_start_square(self, square, mode):
        """
        Returns the first square in the word containing the given square.
        """
        return self.get_word_squares(square, mode)[0]

    def get_clue(self, square, mode):
        """
        Returns the clue for the word containing the given square.
        """
        if self.is_block(square):
            return ""
        start = self.get_word_start_square(square, mode)
        return self.clues[str(mode)].get(str(start), "")

    def set_clue(self, square, mode, clue):
        """
        Sets the clue for the word containing the given square.
        """
        if self.is_block(square):
            return
        start = self.get_word_start_square(square, mode)
        self.clues[str(mode)][str(start)] = clue

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

    def save(self, filename):
        """
        Saves the grid to a file.
        """
        import json

        data = {"size": self.size, "squares": self.squares, "clues": self.clues}
        with open(filename, "w+") as f:
            json.dump(data, f, indent=4)

    def print(self):
        for row in self.squares:
            print("".join([char if char != "" else " " for char in row]))
