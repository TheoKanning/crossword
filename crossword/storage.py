def save(crossword, filename):
    """
    Saves a crossword as a txt file with the given name
    """

    with open(filename, 'w+') as f:
        for line in crossword:
            f.write(''.join([char if char != '' else ' ' for char in line]))
            f.write('\n')


def load(filename):
    """
    Loads a crossword stored in the given txt file and returns it as an array
    """
    crossword = []

    with open(filename, 'r') as f:
        for line in f.readlines():
            crossword.append([char if char != ' ' else '' for char in line if char != '\n'])

    return crossword
