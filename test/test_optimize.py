import unittest

from crossword.grid import Grid
from crossword import optimize


squares = [
    ['.', '.', 'I', 'D', 'K'],
    ['A', 'W', 'F', 'U', 'L'],
    ['P', '.', '', 'C', 'E'],
    ['S', 'L', 'A', 'T', 'E'],
    ['E', 'E', 'R', '.', '.']
]


class OptimizeTests(unittest.TestCase):

    def test_clear_letters(self):
        grid = Grid(squares)

        grid = optimize._clear_letters((0, 2), (0, 2), grid)
        self.assertEqual(grid.get_square((0, 0)), '.')
        self.assertEqual(grid.get_square((0, 1)), '.')
        self.assertEqual(grid.get_square((1, 0)), '')
        self.assertEqual(grid.get_square((1, 1)), '')
