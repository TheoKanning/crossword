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
        print("Could not find dictionary file: " + DICTIONARY)
        return []

    word = word.lower()
    regex = '^' + word.replace(' ','.') + ";.*$" # replace wildcards, enforce start and stop

    with open(DICTIONARY) as f:
        text = f.read()
        words = [word.split(';') for word in re.findall(regex, text, re.MULTILINE)]
        words.sort(key=lambda x: x[1], reverse=True)
        return words[:50]

