import unittest

from parameterized import parameterized

from crossword.grid import Grid, Mode

squares = [
    [".", ".", "I", "D", "K"],
    ["A", "W", "F", "U", "L"],
    ["P", ".", "", "C", "E"],
    ["S", "L", "A", "T", "E"],
    ["E", "E", "R", ".", "."],
]


class GridTests(unittest.TestCase):
    def test_mode_toggle(self):
        mode = Mode.ACROSS
        self.assertEqual(mode.opposite(), Mode.DOWN)

        mode = Mode.DOWN
        self.assertEqual(mode.opposite(), Mode.ACROSS)

    def test_raise_error_if_not_square(self):
        with self.assertRaises(AssertionError):
            Grid([[""], ["", ""]], 3)

    def test_create_empty_grid(self):
        grid = Grid(None, 2)
        self.assertEqual(grid.squares, [["", ""], ["", ""]])
        self.assertEqual(grid.size, 2)

    def test_copy(self):
        grid = Grid(squares)
        copy = grid.copy()

        grid.set_square((2, 2), "X")
        self.assertEqual(grid.get_square((2, 2)), "X")
        self.assertEqual(copy.get_square((2, 2)), "")

    @parameterized.expand([[(0, 0), "."], [(1, 2), "F"], [(2, 2), ""]])
    def test_get_square(self, square, expected):
        grid = Grid(squares, 5)
        self.assertEqual(grid.get_square(square), expected)

    @parameterized.expand(
        [[(0, 0), "A", "A"], [(1, 2), "b", "B"], [(2, 0), ".", "."], [(4, 3), "", ""]]
    )
    def test_set_square(self, square, text, expected):
        grid = Grid(squares, 5)
        grid.set_square(square, text)
        self.assertEqual(grid.get_square(square), expected)

    def test_is_empty(self):
        grid = Grid(squares, 5)
        self.assertTrue(grid.is_empty((2, 2)))
        self.assertFalse(grid.is_empty((0, 2)))

    def test_is_block(self):
        grid = Grid(squares, 5)
        self.assertTrue(grid.is_block((2, 1)))
        self.assertFalse(grid.is_block((3, 3)))

    def test_is_complete(self):
        grid = Grid(squares)
        self.assertFalse(grid.is_complete())

        grid.set_square((2, 2), "A")
        self.assertTrue(grid.is_complete())

    @parameterized.expand(
        [
            [(0, 0), Mode.ACROSS, []],
            [(1, 0), Mode.ACROSS, [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4)]],
            [(2, 0), Mode.ACROSS, [(2, 0)]],
            [(2, 2), Mode.ACROSS, [(2, 2), (2, 3), (2, 4)]],
            [(0, 0), Mode.DOWN, []],
            [(1, 0), Mode.DOWN, [(1, 0), (2, 0), (3, 0), (4, 0)]],
            [(2, 2), Mode.DOWN, [(0, 2), (1, 2), (2, 2), (3, 2), (4, 2)]],
            [(4, 1), Mode.DOWN, [(3, 1), (4, 1)]],
        ]
    )
    def test_get_word_squares(self, square, mode, expected):
        grid = Grid(squares, 5)
        actual = grid.get_word_squares(square, mode)
        self.assertEqual(actual, expected)

    @parameterized.expand(
        [
            [(0, 0), Mode.ACROSS, ""],
            [(1, 0), Mode.ACROSS, "AWFUL"],
            [(2, 0), Mode.ACROSS, "P"],
            [(2, 2), Mode.ACROSS, " CE"],
            [(0, 0), Mode.DOWN, ""],
            [(1, 0), Mode.DOWN, "APSE"],
            [(2, 2), Mode.DOWN, "IF AR"],
            [(4, 1), Mode.DOWN, "LE"],
        ]
    )
    def test_get_word(self, square, mode, expected):
        grid = Grid(squares, 5)
        actual = grid.get_word(square, mode)
        self.assertEqual(actual, expected)

    @parameterized.expand(
        [
            [(0, 2), Mode.ACROSS, (0, 2)],
            [(0, 4), Mode.ACROSS, (0, 2)],
            [(1, 2), Mode.ACROSS, (1, 0)],
            [(2, 2), Mode.ACROSS, (2, 2)],
            [(0, 4), Mode.DOWN, (0, 4)],
            [(1, 0), Mode.DOWN, (1, 0)],
            [(3, 0), Mode.DOWN, (1, 0)],
            [(4, 1), Mode.DOWN, (3, 1)],
        ]
    )
    def test_get_word_start_square(self, square, mode, expected):
        grid = Grid(squares, 5)
        actual = grid.get_word_start_square(square, mode)
        self.assertEqual(expected, actual)

    def test_set_and_get_clue(self):
        grid = Grid(squares, 5)
        grid.set_clue((0, 2), Mode.ACROSS, "Clue 1")

        self.assertEqual("Clue 1", grid.get_clue((0, 2), Mode.ACROSS))
        self.assertEqual("Clue 1", grid.get_clue((0, 4), Mode.ACROSS))
        self.assertEqual("", grid.get_clue((0, 2), Mode.DOWN))

        grid.set_clue((2, 2), Mode.DOWN, "Clue 2")

        self.assertEqual("Clue 2", grid.get_clue((2, 2), Mode.DOWN))
        self.assertEqual("Clue 2", grid.get_clue((0, 2), Mode.DOWN))
        self.assertEqual("Clue 2", grid.get_clue((4, 2), Mode.DOWN))
        self.assertEqual("", grid.get_clue((2, 2), Mode.ACROSS))

    def test_get_all_words(self):
        squares = [
            [".", "", "", "", ""],
            ["", "", "", "", ""],
            ["", "", ".", "", ""],
            ["", "", "", "", ""],
            ["", "", "", "", "."],
        ]
        grid = Grid(squares, 5)
        words = grid.get_all_words()

        across = [w[0] for w in words if w[1] == Mode.ACROSS]
        self.assertEqual(across, [(0, 1), (1, 0), (2, 0), (2, 3), (3, 0), (4, 0)])

        down = [w[0] for w in words if w[1] == Mode.DOWN]
        self.assertEqual(down, [(0, 1), (0, 2), (0, 3), (0, 4), (1, 0), (3, 2)])
