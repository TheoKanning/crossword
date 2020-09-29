from parameterized import parameterized
import time
import unittest

from crossword.dictionary import CrosswordDictionary

class DictionaryTests(unittest.TestCase):

    def setUp(self):
        # use test dictionary since the real one isn't checked in
        self.dictionary = CrosswordDictionary("test/sample_dictionary.txt")

    def test_single_response(self):
        results = self.dictionary.search("bird")
        self.assertEqual(results, [["bird", '50']])

    def test_case_insensitive(self):
        results = self.dictionary.search("bIrD")
        self.assertEqual(results, [["bird", '50']])

    def test_no_response(self):
        results = self.dictionary.search("kdlka")
        self.assertEqual(results, [])

    def test_multiple_responses(self):
        results = self.dictionary.search("bi d")
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
        letters = self.dictionary.get_allowed_letters(word, index)
        self.assertEqual(letters, expected)

    @parameterized.expand([
        [None, ["bind", "bird", "date", "idea", "note", "word"]],
        [1,    ["date", "idea", "word", "bind", "note", "bird"]],
        [2,    ["date", "idea", "bird", "note", "word", "bind"]],
    ])
    def test_seeded_shuffling(self, seed, expected):
        dictionary = CrosswordDictionary("test/sample_dictionary.txt", seed)
        words = [w[0] for w in dictionary.search("    ")]
        self.assertEqual(words, expected)
