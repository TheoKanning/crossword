import unittest

from parameterized import parameterized

from crossword import grid
from crossword.model import Model, Background

squares = [
    [".", ".", "I", "D", "K"],
    ["A", "W", "F", "U", "L"],
    ["P", ".", "", "C", "E"],
    ["S", "L", "A", "T", "E"],
    ["E", "E", "R", ".", "."],
]

dictionary_path = "test/dictionaries/"


class ModelTests(unittest.TestCase):
    def test_create_from_squares(self):
        model = Model(squares, dictionary_path=dictionary_path)
        self.assertEqual(model.size, 5)

    def test_create_from_file(self):
        model = Model(filename="test/crossword.txt", dictionary_path=dictionary_path)
        self.assertEqual(model.size, 15)

    def test_create_from_size(self):
        model = Model(size=8, dictionary_path=dictionary_path)
        self.assertEqual(model.size, 8)

    def test_toggle(self):
        model = Model(squares, dictionary_path=dictionary_path)
        model.mode = grid.Mode.ACROSS
        model.focus = (3, 1)

        model.toggle_orientation()
        self.assertEqual(model.mode, grid.Mode.DOWN)
        self.assertEqual(model.highlight, [(3, 1), (4, 1)])

    @parameterized.expand(
        [
            [(0, 0), grid.Mode.ACROSS, []],
            [(1, 0), grid.Mode.ACROSS, [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4)]],
            [(2, 0), grid.Mode.ACROSS, [(2, 0)]],
            [(2, 2), grid.Mode.ACROSS, [(2, 2), (2, 3), (2, 4)]],
            [(0, 0), grid.Mode.DOWN, []],
            [(1, 0), grid.Mode.DOWN, [(1, 0), (2, 0), (3, 0), (4, 0)]],
            [(2, 2), grid.Mode.DOWN, [(0, 2), (1, 2), (2, 2), (3, 2), (4, 2)]],
            [(4, 1), grid.Mode.DOWN, [(3, 1), (4, 1)]],
        ]
    )
    def test_update_highlighted_squares(self, focus, mode, highlight):
        model = Model(squares, dictionary_path=dictionary_path)
        model.mode = mode
        model.update_focus(focus[0], focus[1])
        self.assertEqual(model.focus, focus)
        self.assertEqual(model.highlight, highlight)

    @parameterized.expand(
        [
            [(0, 0), ".", Background.BLACK, False],
            [(1, 1), "W", Background.WHITE, False],
            [(2, 2), "", Background.HIGHLIGHT, False],
            [(2, 3), "C", Background.HIGHLIGHT, True],
        ]
    )
    def test_get_square_info(self, square, text, background, focused):
        model = Model(squares, dictionary_path=dictionary_path)
        model.update_focus(2, 3)
        actual = model.get_square(square[0], square[1])
        self.assertEqual(actual.text, text)
        self.assertEqual(actual.background, background)
        self.assertEqual(actual.focused, focused)

    @parameterized.expand(
        [
            [(0, 2), "A", grid.Mode.ACROSS, (0, 3)],
            [(0, 4), "A", grid.Mode.ACROSS, (0, 4)],
            [(1, 2), ".", grid.Mode.ACROSS, (1, 3)],
            [(2, 0), "A", grid.Mode.ACROSS, (2, 1)],
            [(3, 1), "", grid.Mode.ACROSS, (3, 0)],
            [(0, 2), "A", grid.Mode.DOWN, (1, 2)],
            [(4, 0), "A", grid.Mode.DOWN, (4, 0)],
            [(1, 1), "A", grid.Mode.DOWN, (2, 1)],
            [(3, 4), "", grid.Mode.DOWN, (2, 4)],
        ]
    )
    def test_get_next_focus(self, current_focus, text, mode, new_focus):
        model = Model(squares, dictionary_path=dictionary_path)
        model.mode = mode
        model.focus = current_focus
        model.get_next_focus(text)
        self.assertEqual(model.focus, new_focus)

    def test_update_square_block_symmetry(self):
        model = Model(squares, dictionary_path=dictionary_path)
        model.update_square(4, 0, grid.BLOCK)

        self.assertEqual(model.get_square(4, 0).text, grid.BLOCK)
        self.assertEqual(model.get_square(0, 4).text, grid.BLOCK)

        model.update_square(0, 4, "A")

        self.assertEqual(model.get_square(4, 0).text, "")
        self.assertEqual(model.get_square(0, 4).text, "A")

    def test_movement(self):
        model = Model(squares, dictionary_path=dictionary_path)
        model.focus = (2, 2)

        model.move_up()
        self.assertEqual(model.focus, (1, 2))

        model.move_left()
        self.assertEqual(model.focus, (1, 1))

        model.move_down()
        self.assertEqual(model.focus, (2, 1))

        model.move_right()
        self.assertEqual(model.focus, (2, 2))


if __name__ == "__main__":
    unittest.main()
