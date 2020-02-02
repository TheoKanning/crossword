from os import path
import re
import time

DICTIONARY="dictionary.txt"

def search(word):
    """
    Finds matching words in the dictionary.
    Input: Search word, using spaces for wildcards. e.g. 'letters', or ' et  r '
    Returns (word, score), sorted highest to lowest. Limited to 20 words.
    """
    if not path.exists(DICTIONARY):
        return []

    word = word.lower()
    regex = '^' + word.replace(' ','.') + '$' # replace wildcards, enforce start and stop

    with open(DICTIONARY) as f:
        words = [line[:-1].split(';') for line in f if re.search(regex, line.split(';')[0])]
        words.sort(key=lambda x: x[1], reverse=True)
        return words[:20]

