import os
import unittest

from crossword import search
from crossword.grid import Grid

# advanced search tests that require a full dictionary. Can't be run by ci because the 
# dictionary is not checked in
@unittest.skipIf(os.getenv("CI"), "Dictionary not available on CI server")
class AdvancedSearchTests(unittest.TestCase):

    def test_finish_easy_puzzle(self):
        squares = [
                ['.','.',' ',' ',' '],
                ['B','E','E','C','H'],
                ['A','S','A','H','I'],
                ['T','A','C','O','S'],
                ['H','U','H','.','.']
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
