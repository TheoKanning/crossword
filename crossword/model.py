from collections import namedtuple
from enum import Enum
from os import path

from crossword import storage
from crossword.dictionary import Dictionary
from crossword.grid import BLOCK, Grid, Mode
from crossword.optimize import optimize


class Background(Enum):
    WHITE = 0
    BLACK = 1
    YELLOW = 2


Square = namedtuple('Square', ['text', 'background', 'focused', 'bold'])


class Model:
    """
    A class that holds all of the UI state for a crossword puzzle.
    """

    def __init__(self, squares=None, filename=None, size=15, dictionary_path="dictionaries/"):
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
        self.set_manually = [[not self.grid.is_empty((r, c)) for c in range(self.size)] for r in range(self.size)]
        self.dictionary = Dictionary(dictionary_path)

    def toggle_orientation(self):
        self.mode = self.mode.opposite()
        self.update_highlighted_squares()

    def update_focus(self, row, col):
        self.focus = (row, col)
        self.update_highlighted_squares()

    def save(self, filename):
        storage.save(self.grid.squares, filename)

    def update_square(self, row, col, text):
        # maintain block symmetry
        if text == BLOCK:
            # add corresponding block
            self.grid.set_square((self.size - 1 - row, self.size - 1 - col), BLOCK)
        elif self.grid.get_square((row, col)) == BLOCK and text != BLOCK:
            # remove corresponding block if this square used to be a block
            self.grid.set_square((self.size - 1 - row, self.size - 1 - col), '')
        self.grid.set_square((row, col), text)
        self.set_manually[row][col] = text != ''
        self.get_next_focus(text)
        self.update_highlighted_squares()

    def get_square(self, row, col):
        text = self.grid.get_square((row, col))
        background = Background.WHITE
        if text == BLOCK:
            background = Background.BLACK
        elif (row, col) in self.highlight:
            background = Background.YELLOW
        focused = (row, col) == self.focus
        bold = self.set_manually[row][col]
        return Square(text, background, focused, bold)

    def update_highlighted_squares(self):
        self.highlight = self.grid.get_word_squares(self.focus, self.mode)

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
        # prioritizes words that use a letter compatible with crossing words
        # (across, down), each is a list of tuples (word, score)

        if self.grid.get_square(self.focus) == BLOCK:
            return [], []

        across = self._get_suggestions(self.focus, Mode.ACROSS)
        down = self._get_suggestions(self.focus, Mode.DOWN)

        return across, down

    def _get_suggestions(self, square, mode):
        word = self.grid.get_word(square, mode)
        squares = self.grid.get_word_squares(square, mode)

        # copy to avoid modifying cached lists
        words = self.dictionary.search(word).copy()
        compatible_words = words.copy()

        # loop through empty letter index and remove words that don't fit crossing words
        for i, s in enumerate(squares):
            if not self.grid.is_empty(s):
                # skip squares that are already filled in
                continue

            cross_index = self.grid.get_word_squares(s, mode.opposite()).index(s)
            cross_word = self.grid.get_word(s, mode.opposite())
            available_letters = self.dictionary.get_allowed_letters(cross_word, cross_index)
            compatible_words = [w for w in compatible_words if w[0][i] in available_letters]

        # add bonus to compatible words
        for i, w in enumerate(words):
            if w in compatible_words:
                words[i] = w[0], str(int(w[1]) + 100)

        words.sort(key=lambda w: int(w[1]), reverse=True)
        return words

    def fill(self):
        """ Fill in any blank squares. Letters not set manually will appear gray """
        grid = self.grid.copy()

        # clear any squares set by previous fills
        for r in range(self.size):
            for c in range(self.size):
                if not self.set_manually[r][c]:
                    grid.set_square((r, c), '')
        filled_grid, _ = optimize(grid, self.dictionary)
        self.grid = filled_grid

    def print(self):
        self.grid.print()
