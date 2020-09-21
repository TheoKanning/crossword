from os import path
import re
import time

DICTIONARY="dictionary.txt"
# tracking this in a boolean is dumb, but it works for tests that use either dictionary
initialized = False

def create_dictionaries():
    for n in range(3, 22):
        with open(f"dictionary/{n}.txt", 'w') as f:
            f.writelines('\n'.join(_search_file(' '*n, DICTIONARY)))

    global initialized
    initialized = True

def search(word, limit=1000):
    """
    Finds matching words in the dictionary.
    Input: Search word, using spaces for wildcards. e.g. 'letters', or ' et  r '
    Returns (word, score), sorted highest to lowest. Limited to 20 words.
    """
    if not initialized:
        print("Creating dictionaries")
        create_dictionaries()

    filename = f"dictionary/{len(word)}.txt"
    if not path.exists(filename):
        print(f"Could not find dictionary file:{filename}")
        return []

    word = word.lower()

    words = [word.split(';') for word in _search_file(word, filename)]
    words.sort(key=lambda x: x[1], reverse=True)
    return words[:limit]

def get_allowed_letters(word, index):
    """
    Returns a list of letters that can go at the specified index of the word
    """
    words = search(word)
    return set([w[0][index] for w in words])

def _search_file(word, filename):
    regex = '^' + word.replace(' ','.') + ";.*$" # replace wildcards, enforce start and stop

    with open(filename) as f:
        text = f.read()
        words = re.findall(regex, text, re.MULTILINE)

    return words
