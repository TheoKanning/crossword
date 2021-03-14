import os
from parameterized import parameterized
import unittest


from crossword import grid
from crossword.model import Model, Background

squares = [
    ['.', '.', 'I', 'D', 'K'],
    ['A', 'W', 'F', 'U', 'L'],
    ['P', '.', '', 'C', 'E'],
    ['S', 'L', 'A', 'T', 'E'],
    ['E', 'E', 'R', '.', '.']
]


# advanced suggestion tests that require a full dictionary. Can't be run by ci because the
# dictionary is not checked in
@unittest.skipIf(os.getenv("CI"), "Dictionary not available on CI server")
class ModelTests(unittest.TestCase):

    def test_suggestions(self):
        squares = [
            ['.', '.', ' ', ' ', ' '],
            ['B', 'E', 'E', 'C', 'H'],
            ['A', 'S', 'A', 'H', 'I'],
            ['T', 'A', 'C', 'O', 'S'],
            ['H', 'U', 'H', '.', '.']
        ]
        model = Model(squares)
        model.update_focus(0,2)
        across, down = model.get_suggestions()

    def test_suggestions(self):
        squares = [
            ['.', '.', '', '', ''],
            ['B', 'E', 'E', 'C', 'H'],
            ['A', 'S', 'A', 'H', 'I'],
            ['T', 'A', 'C', 'O', 'S'],
            ['H', 'U', 'H', '.', '.']
        ]
        model = Model(squares)
        suggestions = model._get_suggestions((0,2), grid.Mode.ACROSS)
        print(suggestions[:10])

if __name__ == "__main__":
    unittest.main()
