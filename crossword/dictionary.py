import os
import random
import re
from functools import lru_cache


class Dictionary:

    def __init__(self, directory="dictionaries/", seed=None):
        self.dictionaries = {}
        self.create_dictionaries(directory, seed)

    def create_dictionaries(self, directory, seed=None):
        """
        Break the dictionary file into a separate in-memory dictionary for each possible length
        Sorts word by value here so they don't have to be sorted again later
        """
        files = os.listdir(directory)
        contents = []
        for filename in files:
            with open(os.path.join(directory, filename)) as f:
                contents.append(f.read())

        text = '\n'.join(contents)

        for n in range(3, 22):
            words = self._search_text(' ' * n, text)

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
        if len(word) < 3 or len(word) > 22:
            return []

        word = word.lower()

        words = [w.split(';') for w in self._search_text(word, self.dictionaries[len(word)])]
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
        regex = '^' + word.replace(' ', '.') + ";.*$"  # replace wildcards, enforce start and stop
        return re.findall(regex, text, re.MULTILINE)


if __name__ == "__main__":
    import sys
    query = sys.argv[1]
    dictionary = Dictionary()
    for word in dictionary.search(query):
        print(word)
