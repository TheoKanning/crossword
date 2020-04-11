from parameterized import parameterized
import unittest
from context import dictionary
from context import model
from context import storage

squares = [
           ['.','.','I','D','K'],
           ['A','W','F','U','L'],
           ['P','.','','C','E'],
           ['S','L','A','T','E'],
           ['E','E','R','.','.']
   ]

class CrosswordTests(unittest.TestCase):


    def test_not_square(self):
        with self.assertRaises(AssertionError):
            model.Puzzle([[''],['']], 'filename')

    @parameterized.expand([
        [(0,0), model.Mode.HORIZONTAL, []],
        [(1,0), model.Mode.HORIZONTAL, [(1,0), (1,1), (1,2), (1,3), (1,4)]],
        [(2,0), model.Mode.HORIZONTAL, [(2,0)]],
        [(2,2), model.Mode.HORIZONTAL, [(2,2), (2,3), (2,4)]],
        [(0,0), model.Mode.VERTICAL, []],
        [(1,0), model.Mode.VERTICAL, [(1,0), (2,0), (3,0), (4,0)]],
        [(2,2), model.Mode.VERTICAL, [(0,2), (1,2), (2,2), (3,2), (4,2)]],
        [(4,1), model.Mode.VERTICAL, [(3,1), (4,1)]],
        ])
    def test_update_highlighted_squares(self, focus, mode, highlight):
        puzzle = model.Puzzle(squares)
        puzzle.mode = mode
        puzzle.update_focus(focus[0], focus[1])
        self.assertEqual(puzzle.focus, focus)
        self.assertEqual(puzzle.highlight, highlight)

    @parameterized.expand([
        [(0,0), '.', model.Background.BLACK, False],
        [(1,1), 'W', model.Background.WHITE, False],
        [(2,2), '', model.Background.YELLOW, False],
        [(2,3), 'C', model.Background.YELLOW, True]
        ])
    def test_get_square_info(self, square, text, background, focused):
        puzzle = model.Puzzle(squares)
        puzzle.update_focus(2, 3)
        actual = puzzle.get_square(square[0], square[1])
        self.assertEqual(actual.text, text)
        self.assertEqual(actual.background, background)
        self.assertEqual(actual.focused, focused)

    @parameterized.expand([
        [ 8,  0, model.Mode.HORIZONTAL, "E  ET"],
        [11, 14, model.Mode.HORIZONTAL, "LENT"],
        [ 6,  5, model.Mode.HORIZONTAL, "LASER"],
        [ 8,  0, model.Mode.HORIZONTAL, "E  ET"],
        [ 7,  2, model.Mode.VERTICAL,"G ANDEUR"],
        [ 8,  4, model.Mode.VERTICAL,  "CANTOR"],
        ])
    def test_get_word(self, row, col, mode, word):
        crossword = storage.load("tests/crossword.txt")
        puzzle = model.Puzzle(crossword)
        puzzle.mode = mode
        actual = puzzle.get_word(row, col)
        self.assertEqual(actual, word)

    @parameterized.expand([
        [(0, 2), 'A', model.Mode.HORIZONTAL, (0, 3)],
        [(0, 4), 'A', model.Mode.HORIZONTAL, (1, 0)],
        [(1, 2), '.', model.Mode.HORIZONTAL, (1, 3)],
        [(2, 0), 'A', model.Mode.HORIZONTAL, (2, 2)],
        [(3, 1),  '', model.Mode.HORIZONTAL, (3, 1)],
        [(4, 2), 'A', model.Mode.HORIZONTAL, (0, 2)],
        [(0, 2), 'A', model.Mode.VERTICAL, (1, 2)],
        [(4, 0), 'A', model.Mode.VERTICAL, (1, 1)],
        [(1, 1), 'A', model.Mode.VERTICAL, (3, 1)],
        [(3, 4), 'A', model.Mode.VERTICAL, (1, 0)]
        ])
    def test_get_next_focus(self, current_focus, text, mode, new_focus):
        puzzle = model.Puzzle(squares)
        puzzle.mode = mode
        puzzle.update_square(current_focus[0], current_focus[1], text)
        self.assertEqual(puzzle.focus, new_focus)

if __name__ == "__main__":
    unittest.main()

