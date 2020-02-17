from parameterized import parameterized
import unittest
from context import dictionary
from context import storage
from context import words

class CrosswordTests(unittest.TestCase):

    def test_not_square(self):
        with self.assertRaises(AssertionError):
            words.Puzzle([[''],['']], 'filename')

    @parameterized.expand([
        [(0,0), [(0,0), (0,1), (0,2)]],
        [(5,9), [(5,8), (5,9), (5,10)]],
        [(5,14), [(5,12), (5,13), (5,14)]],
        ])
    def test_get_highlighted_squares(self, coords, expected):
        crossword = storage.load("tests/crossword.txt")
        actual = words.get_highlighted_squares(crossword, coords[0], coords[1])
        self.assertEqual(actual, expected)

    @parameterized.expand([
        ["abc.defgh.ijklm", 1, (0,2)],
        ["abc.defgh.ijklm", 4, (4,8)],
        ["abc.defgh.ijklm", 5, (4,8)],
        ["abc.defgh.ijklm", 8, (4,8)],
        ["abc.defgh.ijklm", 10, (10,14)],
        ["abc.defgh.ijklm", 14, (10,14)]
        ])
    def test_highlighted_indices(self, word, index, expected):
        actual = words.get_highlighted_indices(word, index)
        self.assertEqual(actual, expected)

    @parameterized.expand([
        [8, 0, "E  ET"],
        [11, 14, "LENT"],
        [6, 5, "LASER"]
        ])
    def test_get_word(self, row, col, word):
        crossword = storage.load("tests/crossword.txt")
        actual = words.get_word(crossword, row, col)
        self.assertEqual(actual, word)

if __name__ == "__main__":
    unittest.main()

