import unittest
from context import storage

class StorageTests(unittest.TestCase):

    def test_save_and_load(self):
        crossword = [
                ['#','#','I','D','K'],
                ['A','W','F','U','L'],
                ['P','I',' ','C','E'],
                ['S','L','A','T','E'],
                ['E','E','R','#','#']
        ]

        storage.save(crossword, 'tests/test_crossword.txt')

        saved = storage.load('tests/test_crossword.txt')
        self.assertEqual(saved, crossword)

if __name__ == '__main__':
    unittest.main()

