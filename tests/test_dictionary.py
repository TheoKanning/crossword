import unittest
from context import dictionary

class DictionaryTests(unittest.TestCase):

    def test_single_response(self):
        results = dictionary.search("bird")
        self.assertEqual(results, [["bird", '50']])

    def test_no_response(self):
        results = dictionary.search("kdlka")
        self.assertEqual(results, [])

    def test_multiple_responses(self):
        results = dictionary.search("bi d")
        expected = [
                ['bigd', '50'],
                ['bind', '50'],
                ['bird', '50']
            ]
        self.assertEqual(results, expected)

if __name__ == '__main__':
    unittest.main()

