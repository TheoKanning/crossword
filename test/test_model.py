from parameterized import parameterized
import unittest
from crossword import model
from crossword import storage

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
        [(0,0), model.Mode.ACROSS, []],
        [(1,0), model.Mode.ACROSS, [(1,0), (1,1), (1,2), (1,3), (1,4)]],
        [(2,0), model.Mode.ACROSS, [(2,0)]],
        [(2,2), model.Mode.ACROSS, [(2,2), (2,3), (2,4)]],
        [(0,0), model.Mode.DOWN, []],
        [(1,0), model.Mode.DOWN, [(1,0), (2,0), (3,0), (4,0)]],
        [(2,2), model.Mode.DOWN, [(0,2), (1,2), (2,2), (3,2), (4,2)]],
        [(4,1), model.Mode.DOWN, [(3,1), (4,1)]],
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
        [ 8,  0, model.Mode.ACROSS, "E  ET"],
        [11, 14, model.Mode.ACROSS, "LENT"],
        [ 6,  5, model.Mode.ACROSS, "LASER"],
        [ 8,  0, model.Mode.ACROSS, "E  ET"],
        [ 7,  2, model.Mode.DOWN,"G ANDEUR"],
        [ 8,  4, model.Mode.DOWN,  "CANTOR"],
        ])
    def test_get_word(self, row, col, mode, word):
        crossword = storage.load("test/crossword.txt")
        puzzle = model.Puzzle(crossword)
        puzzle.mode = mode
        actual = puzzle.get_word(row, col)
        self.assertEqual(actual, word)

    @parameterized.expand([
        [(0, 2), 'A', model.Mode.ACROSS, (0, 3)],
        [(0, 4), 'A', model.Mode.ACROSS, (0, 4)],
        [(1, 2), '.', model.Mode.ACROSS, (1, 3)],
        [(2, 0), 'A', model.Mode.ACROSS, (2, 1)],
        [(3, 1),  '', model.Mode.ACROSS, (3, 0)],
        [(0, 2), 'A', model.Mode.DOWN, (1, 2)],
        [(4, 0), 'A', model.Mode.DOWN, (4, 0)],
        [(1, 1), 'A', model.Mode.DOWN, (2, 1)],
        [(3, 4),  '', model.Mode.DOWN, (2, 4)]
        ])
    def test_get_next_focus(self, current_focus, text, mode, new_focus):
        puzzle = model.Puzzle(squares)
        puzzle.mode = mode
        puzzle.focus = current_focus
        puzzle.get_next_focus(text)
        self.assertEqual(puzzle.focus, new_focus)

    def test_update_square_block_symmetry(self):
        puzzle = model.Puzzle(squares)
        puzzle.update_square(4, 0, model.BLOCK)

        self.assertEqual(puzzle.get_square(4, 0).text, model.BLOCK)
        self.assertEqual(puzzle.get_square(0, 4).text, model.BLOCK)

        puzzle.update_square(0, 4, 'A')

        self.assertEqual(puzzle.get_square(4, 0).text, '')
        self.assertEqual(puzzle.get_square(0, 4).text, 'A')

    def test_movement(self):
        puzzle = model.Puzzle(squares)
        puzzle.focus = (2, 2)

        puzzle.move_up()
        self.assertEqual(puzzle.focus, (1, 2))

        puzzle.move_left()
        self.assertEqual(puzzle.focus, (1, 1))

        puzzle.move_down()
        self.assertEqual(puzzle.focus, (2, 1))

        puzzle.move_right()
        self.assertEqual(puzzle.focus, (2, 2))

if __name__ == "__main__":
    unittest.main()

