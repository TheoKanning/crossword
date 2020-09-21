from functools import lru_cache
from os import path
import re
import time

DICTIONARY="dictionary.txt"
# tracking this in a boolean is dumb, but it works for tests that use either dictionary
initialized = False
dictionaries = {}

def create_dictionaries():
    """
    Break the big dicitonary file into a separate in-memory dictionary for each possible length
    Sorts word by value here so they don't have to be sorted again later
    """
    global dictionaries, initialized
    with open(DICTIONARY) as f:
        text = f.read()
        for n in range(3, 22):
            words = _search_text(' '*n, text)
            words.sort(key=lambda x: x.split(';')[1], reverse=True)
            dictionaries[n] = '\n'.join(words)

    initialized = True

@lru_cache(maxsize=32)
def search(word, limit=1000):
    """
    Finds matching words in the dictionary.
    Input: Search word, using spaces for wildcards. e.g. 'letters', or ' et  r '
    Returns (word, score), sorted highest to lowest. Limited to 20 words.
    """
    if not initialized:
        print("Creating dictionaries")
        create_dictionaries()

    word = word.lower()

    words = [word.split(';') for word in _search_text(word, dictionaries[len(word)])]
    return words[:limit]

def get_allowed_letters(word, index):
    """
    Returns a list of letters that can go at the specified index of the word
    """
    words = search(word)
    return set([w[0][index] for w in words])

def _search_text(word, text):
    """
    Finds rows matching the given word. text is a list of dictionary strings
    """
    regex = '^' + word.replace(' ','.') + ";.*$" # replace wildcards, enforce start and stop
    return re.findall(regex, text, re.MULTILINE)

