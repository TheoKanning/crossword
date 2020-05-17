from collections import namedtuple
from copy import deepcopy
from enum import Enum

from crossword import dictionary

class Mode(Enum):
    ACROSS = 0
    DOWN = 1

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
    def __init__(self, squares=None, filename=None):
        if squares:
            assert len(squares) == len(squares[0])
        else:
            squares = [['' for i in range(0,15)] for j in range(0,15)]
        self.size = len(squares)
        self.squares = deepcopy(squares)
        self.filename = filename
        self.focus = (0, 0)
        self.highlight = []
        self.mode = Mode.ACROSS

    def toggle_orientation(self):
        self.mode = Mode.DOWN if self.mode is Mode.ACROSS else Mode.ACROSS
        self.highlight = self.get_highlighted_squares(self.focus[0], self.focus[1])

    def update_focus(self, row, col):
        self.focus = (row, col)
        self.highlight = self.get_highlighted_squares(row, col)

    def update_square(self, row, col, text):
        # maintain block symmetry
        if text == BLOCK:
            self.squares[self.size - 1 - row][self.size - 1 - col] = BLOCK
        elif self.squares[row][col] == BLOCK and text != BLOCK:
            self.squares[self.size - 1 - row][self.size - 1 - col] = ''
        self.squares[row][col] = text
        self.get_next_focus(text)
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

    def get_word(self, row, col, mode):
        """
        Finds the word containing the given square
        """
        squares = self.get_highlighted_squares(row, col, mode)
        chars = [self.squares[square[0]][square[1]] for square in squares]
        return ''.join([char if char != '' else ' ' for char in chars])

    def get_highlighted_squares(self, row, col, mode=None):
        """
        Return the coordinates of all of the squares that form a continuous word
        with the given square.
        """
        if self.squares[row][col] == BLOCK:
            return []

        if not mode:
            mode = self.mode

        highlighted = []
        horizontal = mode is Mode.ACROSS
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

    def get_next_focus(self, text):
        """
        Get the coordinates of the square that should be focused after the given square
        """
        if text == '':
            # text was deleted, go backwards
            if self.mode is Mode.ACROSS:
                self.move_left()
            else:
                self.move_up()
        else:
            # text was added
            if self.mode is Mode.ACROSS:
                self.move_right()
            else:
                self.move_down()

    def move_up(self):
        self.focus = (max(0, self.focus[0] - 1), self.focus[1])

    def move_down(self):
        self.focus = (min(self.size - 1, self.focus[0] + 1), self.focus[1])

    def move_left(self):
        self.focus = (self.focus[0], max(0, self.focus[1] - 1))

    def move_right(self):
        self.focus = (self.focus[0], min(self.size - 1, self.focus[1] + 1))

    def get_suggestions(self):
        # returns suggestions for the focused square
        # (across, down), each is a list of tuples (word, score)

        if self.squares[self.focus[0]][self.focus[1]] == BLOCK:
            return ([], [])

        across_squares = self.get_highlighted_squares(self.focus[0], self.focus[1], Mode.ACROSS)
        across_index = across_squares.index(self.focus)
        across_word = self.get_word(self.focus[0], self.focus[1], Mode.ACROSS)
        down_squares = self.get_highlighted_squares(self.focus[0], self.focus[1], Mode.DOWN)
        down_index = down_squares.index(self.focus)
        down_word = self.get_word(self.focus[0], self.focus[1], Mode.DOWN)

        across_suggestions = dictionary.search(across_word)
        down_suggestions = dictionary.search(down_word)

        across_letters = set([word[0][across_index] for word in across_suggestions])
        down_letters = set([word[0][down_index] for word in down_suggestions])

        for i, word in enumerate(across_suggestions):
            if word[0][across_index] in down_letters:
                across_suggestions[i] = word[0], str(int(word[1]) + 22)

        for i, word in enumerate(down_suggestions):
            if word[0][down_index] in across_letters:
                down_suggestions[i] = word[0], str(int(word[1]) + 22)

        across_suggestions.sort(key=lambda x: x[1], reverse=True)
        down_suggestions.sort(key=lambda x: x[1], reverse=True)

        return across_suggestions, down_suggestions

    def print(self):
        for row in self.squares:
            print( ''.join([char if char != '' else ' ' for char in row]))
