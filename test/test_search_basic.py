import unittest
from crossword import search
from crossword import dictionary
from crossword.grid import Grid, Mode


class BasicSearchTests(unittest.TestCase):

    def setUp(slef):
        dictionary.DICTIONARY="test/sample_dictionary.txt"

    def test_set_word(self):
        grid = Grid()
        word = "ABCDEFGHIJKLMNO"
        search.set_word(grid, (1,2), Mode.ACROSS, word)
        self.assertEqual(grid.get_word((1,2), Mode.ACROSS), word)

    def test_get_next_target(self):
        squares = [
                ['X', 'X', 'X'],
                ['', 'X', ''],
                ['X', '', '']
        ]
        grid = Grid(squares)
        target, direction = search.get_next_target(grid, Mode.ACROSS)
        self.assertEqual(target, (1,0))
        self.assertEqual(direction, Mode.DOWN)

    def test_finish_easy_puzzle(self):
        squares = [
                ['','I','R','D'],
                ['I','X','X','X'],
                ['R','X','X','X'],
                ['D','X','X','X']
        ]
        grid = Grid(squares)
        result = search.search(grid)
        self.assertTrue(result)

    def test_finish_two_step_puzzle(self):
        squares = [
            ['X','X','','X'],
            ['X','X','','X'],
            ['W','','',''],
            ['X','X','','X']
        ]
        grid = Grid(squares)
        result = search.search(grid)
        self.assertTrue(result)

