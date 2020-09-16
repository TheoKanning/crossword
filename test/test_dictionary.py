from parameterized import parameterized
import unittest
from crossword import dictionary

class DictionaryTests(unittest.TestCase):

    def setUp(self):
        # use test dictionary since the real one isn't checked in
        dictionary.DICTIONARY="test/sample_dictionary.txt"

    def test_single_response(self):
        results = dictionary.search("bird")
        self.assertEqual(results, [["bird", '50']])

    def test_case_insensitive(self):
        results = dictionary.search("bIrD")
        self.assertEqual(results, [["bird", '50']])

    def test_no_response(self):
        results = dictionary.search("kdlka")
        self.assertEqual(results, [])

    def test_multiple_responses(self):
        results = dictionary.search("bi d")
        expected = [
                ['bind', '50'],
                ['bird', '50']
            ]
        self.assertEqual(results, expected)

    @parameterized.expand([
        ["bi d", 2, {"n", "r"}],
        ["xx   ", 3, set()],
        ["a ple", 1, {"p"}]
    ])
    def test_allowed_letters(self, word, index, expected):
        letters = dictionary.get_allowed_letters(word, index)
        self.assertEqual(letters, expected)

if __name__ == '__main__':
    unittest.main()

