import unittest

from crossword.dictionary import Dictionary
from crossword.generate import Generator, SearchInfo
from crossword.grid import Grid, Mode


class BasicGeneratorTests(unittest.TestCase):

    def setUp(self):
        dictionary = Dictionary("test/dictionaries")
        self.generator = Generator(dictionary)

    def test_set_word(self):
        grid = Grid()
        word = "ABCDEFGHIJKLMNO"
        self.generator.set_word(grid, (1, 2), Mode.ACROSS, word)
        self.assertEqual(grid.get_word((1, 2), Mode.ACROSS), word)

    def test_get_next_target(self):
        squares = [
            ['X', 'X', 'X'],
            ['', 'X', ''],
            ['X', '', '']
        ]
        grid = Grid(squares)
        info = SearchInfo(unfilled_words = [
            ((1, 0), Mode.ACROSS),
            ((2, 0), Mode.ACROSS),
            ((0, 0), Mode.DOWN),
            ((0, 1), Mode.DOWN),
            ((0, 2), Mode.DOWN)
        ],
        used_words=[])
        target, direction = self.generator.get_next_target(grid, info)
        self.assertEqual(target, (0, 0))
        self.assertEqual(direction, Mode.DOWN)

    def test_get_possible_words(self):
        squares = [
            ['', '', '', ''],
            ['', '', 'O', ''],
            ['', '', 'T', ''],
            ['', '', 'E', '']
        ]
        grid = Grid(squares)
        words = self.generator.get_possible_words(grid, (0, 0), Mode.ACROSS)
        self.assertEqual(words, [("bind", 50)])

    def test_get_possible_words_down(self):
        squares = [
            ['', '', '', ''],
            ['', '', '', ''],
            ['', 'O', 'T', 'E'],
            ['', '', '', '']
        ]
        grid = Grid(squares)
        words = self.generator.get_possible_words(grid, (0, 0), Mode.DOWN)
        self.assertEqual(words, [("bind", 50)])
