import os
import unittest

from crossword.generate import Generator
from crossword.grid import Grid

# advanced search tests that require a full dictionary. Can't be run by ci because the 
# dictionary is not checked in
@unittest.skipIf(os.getenv("CI"), "Dictionary not available on CI server")
class AdvancedGeneratorTests(unittest.TestCase):

    def setUp(self):
        # use default dictionary file, not available on CI
        self.generator = Generator()

    def test_finish_easy_puzzle(self):
        squares = [
                ['.','.',' ',' ',' '],
                ['B','E','E','C','H'],
                ['A','S','A','H','I'],
                ['T','A','C','O','S'],
                ['H','U','H','.','.']
        ]
        grid = Grid(squares)
        result = self.generator.search(grid)
        self.assertTrue(result)

    def test_finish_two_step_puzzle(self):
        squares = [
                ['.','.',' ',' ',' '],
                ['B','E','E','','H'],
                ['A','S','A','H','I'],
                ['T','A','C','','S'],
                ['H','U','H','.','.']
        ]
        grid = Grid(squares)
        result = self.generator.search(grid)
        self.assertTrue(result)
