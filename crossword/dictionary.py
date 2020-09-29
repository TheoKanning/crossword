from functools import lru_cache
from os import path
import random
import re
import time

class CrosswordDictionary:

    def __init__(self, filename="dictionary.txt", seed=None):
        self.dictionaries = {}
        self.create_dictionaries(filename, seed)

    def create_dictionaries(self, filename, seed=None):
        """
        Break the dicitonary file into a separate in-memory dictionary for each possible length
        Sorts word by value here so they don't have to be sorted again later
        """
        with open(filename) as f:
            text = f.read()
            for n in range(3, 22):
                words = self._search_text(' '*n, text)

                if seed is not None:
                    random.seed(seed)
                    random.shuffle(words)

                words.sort(key=lambda x: x.split(';')[1], reverse=True)
                self.dictionaries[n] = '\n'.join(words)

    @lru_cache(maxsize=32)
    def search(self, word, limit=1000):
        """
        Finds matching words in the dictionary.
        Input: Search word, using spaces for wildcards. e.g. 'letters', or ' et  r '
        Returns (word, score), sorted highest to lowest. Limited to 20 words.
        """
        word = word.lower()

        words = [word.split(';') for word in self._search_text(word, self.dictionaries[len(word)])]
        return words[:limit]

    @lru_cache(maxsize=32)
    def get_allowed_letters(self, word, index):
        """
        Returns a list of letters that can go at the specified index of the word
        """
        words = self.search(word)
        return set([w[0][index] for w in words])

    def _search_text(self, word, text):
        """
        Finds rows matching the given word. text is a list of dictionary strings
        """
        regex = '^' + word.replace(' ','.') + ";.*$" # replace wildcards, enforce start and stop
        return re.findall(regex, text, re.MULTILINE)

