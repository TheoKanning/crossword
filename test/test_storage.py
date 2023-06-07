import os
import unittest

from crossword import storage
from crossword.grid import load_grid, Grid, Mode

TEST_FILE = "test_crossword.txt"

crossword = [
    [".", ".", "I", "D", "K"],
    ["A", "W", "F", "U", "L"],
    ["P", "I", "", "C", "E"],
    ["S", "L", "A", "T", "E"],
    ["E", "E", "R", ".", "."],
]


class StorageTests(unittest.TestCase):
    def tearDown(self):
        os.remove(TEST_FILE)

    def test_save_and_load(self):
        storage.save(crossword, TEST_FILE)

        saved = storage.load(TEST_FILE)
        self.assertEqual(saved, crossword)

    def test_save_and_load_grid(self):
        grid = Grid(crossword)
        grid.set_clue((0, 2), Mode.ACROSS, "test clue")

        grid.save(TEST_FILE)

        saved = load_grid(TEST_FILE)
        self.assertEqual(grid.size, saved.size)
        self.assertEqual(grid.squares, saved.squares)
        self.assertEqual(grid.clues, saved.clues)


if __name__ == "__main__":
    unittest.main()
