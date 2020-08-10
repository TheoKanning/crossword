from collections import namedtuple
from enum import Enum
from os import path

from crossword import dictionary, storage
from crossword.grid import BLOCK, Grid, Mode

class Background(Enum):
    WHITE = 0
    BLACK = 1
    YELLOW = 2


Square = namedtuple('Square', ['text', 'background', 'focused'])

class Puzzle:
    """
    A class that holds all of the state for a crossword puzzle.
    """
    def __init__(self, squares=None, filename=None, size=15):
        if squares:
            self.grid = Grid(squares, size)
        elif filename and path.exists(filename):
            squares = storage.load(filename)
            self.grid = Grid(squares)
        else:
            self.grid = Grid(size=size)
        self.size = self.grid.size
        self.focus = (0, 0)
        self.highlight = []
        self.mode = Mode.ACROSS

    def toggle_orientation(self):
        self.mode = Mode.DOWN if self.mode is Mode.ACROSS else Mode.ACROSS
        self.highlight = self.get_highlighted_squares(self.focus[0], self.focus[1])

    def update_focus(self, row, col):
        self.focus = (row, col)
        self.highlight = self.get_highlighted_squares(row, col)

    def save(self, filename):
        storage.save(self.grid.squares, filename)

    def update_square(self, row, col, text):
        # maintain block symmetry
        if text == BLOCK:
            self.grid.set_square((self.size - 1 - row, self.size - 1 - col), BLOCK)
        elif self.grid.get_square((row, col)) == BLOCK and text != BLOCK:
            self.grid.set_square((self.size - 1 - row, self.size - 1 - col), '')
        self.grid.set_square((row,col), text)
        self.get_next_focus(text)
        self.highlight = self.get_highlighted_squares(self.focus[0], self.focus[1])

    def get_square(self, row, col):
        text = self.grid.get_square((row, col))
        background = Background.WHITE
        if text == BLOCK:
            background = Background.BLACK
        elif (row, col) in self.highlight:
            background = Background.YELLOW
        focused = (row, col) == self.focus
        return Square(text, background, focused)

    def get_highlighted_squares(self, row, col, mode=None):
        if not mode:
            mode = self.mode
        return self.grid.get_word_squares((row, col), mode)

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

        if self.grid.get_square(self.focus) == BLOCK:
            return ([], [])

        across_squares = self.get_highlighted_squares(self.focus[0], self.focus[1], Mode.ACROSS)
        across_index = across_squares.index(self.focus)
        across_word = self.grid.get_word(self.focus, Mode.ACROSS)
        down_squares = self.get_highlighted_squares(self.focus[0], self.focus[1], Mode.DOWN)
        down_index = down_squares.index(self.focus)
        down_word = self.grid.get_word(self.focus, Mode.DOWN)

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
        self.grid.print()
