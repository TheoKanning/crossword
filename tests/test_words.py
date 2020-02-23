from parameterized import parameterized
import unittest
from context import dictionary
from context import storage
from context import words

squares = [
           ['.','.','I','D','K'],
           ['A','W','F','U','L'],
           ['P','.',' ','C','E'],
           ['S','L','A','T','E'],
           ['E','E','R','.','.']
   ]

class CrosswordTests(unittest.TestCase):


    def test_not_square(self):
        with self.assertRaises(AssertionError):
            words.Puzzle([[''],['']], 'filename')

    @parameterized.expand([
        [(0,0), []],
        [(1,0), [(1,0), (1,1), (1,2), (1,3), (1,4)]],
        [(2,0), [(2,0)]],
        [(2,2), [(2,2), (2,3), (2,4)]],
        ])
    def test_update_highlighted_squares(self, focus, highlight):
        puzzle = words.Puzzle(squares, "file.txt")
        puzzle.update_focus(focus[0], focus[1])
        self.assertEqual(puzzle.focus, focus)
        self.assertEqual(puzzle.highlight, highlight)

    @parameterized.expand([
        [(0,0), '.', words.BACKGROUND_BLACK, False],
        [(1,1), 'W', words.BACKGROUND_WHITE, False],
        [(2,2), ' ', words.BACKGROUND_YELLOW, False],
        [(2,3), 'C', words.BACKGROUND_YELLOW, True]
        ])
    def test_get_square_info(self, square, text, background, focused):
        puzzle = words.Puzzle(squares, "file.txt")
        puzzle.update_focus(2, 3)
        actual = puzzle.get_square(square[0], square[1])
        self.assertEqual(actual.text, text)
        self.assertEqual(actual.background, background)
        self.assertEqual(actual.focused, focused)

    @parameterized.expand([
        [8, 0, "E  ET"],
        [11, 14, "LENT"],
        [6, 5, "LASER"]
        ])
    def test_get_word(self, row, col, word):
        crossword = storage.load("tests/crossword.txt")
        puzzle = words.Puzzle(crossword, "file.txt")
        actual = puzzle.get_word(crossword, row, col)
        self.assertEqual(actual, word)

if __name__ == "__main__":
    unittest.main()

