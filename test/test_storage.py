import os
import unittest

from crossword import storage

TEST_FILE = "test_crossword.txt"


class StorageTests(unittest.TestCase):
    def tearDown(self):
        os.remove(TEST_FILE)

    def test_save_and_load(self):
        crossword = [
            [".", ".", "I", "D", "K"],
            ["A", "W", "F", "U", "L"],
            ["P", "I", "", "C", "E"],
            ["S", "L", "A", "T", "E"],
            ["E", "E", "R", ".", "."],
        ]

        storage.save(crossword, TEST_FILE)

        saved = storage.load(TEST_FILE)
        self.assertEqual(saved, crossword)


if __name__ == "__main__":
    unittest.main()
