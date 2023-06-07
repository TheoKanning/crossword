import os
import unittest

from crossword import grid
from crossword.model import Model
from test.common import dictionary_path

squares = [
    [".", ".", "I", "D", "K"],
    ["A", "W", "F", "U", "L"],
    ["P", ".", "", "C", "E"],
    ["S", "L", "A", "T", "E"],
    ["E", "E", "R", ".", "."],
]


# advanced suggestion tests that require a full dictionary. Can't be run by ci because the
# dictionary is not checked in
@unittest.skipIf(os.getenv("CI"), "Dictionary not available on CI server")
class ModelTests(unittest.TestCase):
    def test_suggestions(self):
        squares = [
            [".", ".", " ", " ", " "],
            ["B", "E", "E", "C", "H"],
            ["A", "S", "A", "H", "I"],
            ["T", "A", "C", "O", "S"],
            ["H", "U", "H", ".", "."],
        ]
        model = Model(squares, dictionary_path=dictionary_path)
        model.update_focus(0, 2)
        across, down = model.get_suggestions()

    def test_suggestions_across(self):
        squares = [
            [".", ".", "", "", ""],
            ["B", "E", "E", "C", "H"],
            ["A", "S", "A", "H", "I"],
            ["T", "A", "C", "O", "S"],
            ["H", "U", "H", ".", "."],
        ]
        model = Model(squares, dictionary_path=dictionary_path)
        suggestions = model._get_suggestions((0, 2), grid.Mode.ACROSS)
        print(suggestions[:10])

    def test_fill(self):
        squares = [
            [".", ".", "", "", ""],
            ["B", "E", "E", "C", "H"],
            ["A", "S", "A", "H", "I"],
            ["T", "A", "C", "O", "S"],
            ["H", "U", "H", ".", "."],
        ]

        model = Model(squares, dictionary_path=dictionary_path)
        model.fill()

        self.assertEqual([".", ".", "P", "E", "C"], model.grid.squares[0])
        self.assertFalse(model.get_square(0, 2).bold)


if __name__ == "__main__":
    unittest.main()
