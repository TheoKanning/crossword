from copy import deepcopy
from crossword.dictionary import CrosswordDictionary
from crossword.grid import Grid, Mode

class Generator:

    def __init__(self, dictionary):
        self.dictionary = dictionary
        self.nodes_searched = 0

    def get_possible_words(self, grid, square, mode):
        """ Returns a list of all possible words for a given square and direction
            sorted from best to worst
        """
        word = grid.get_word(square, mode)
        words = [w[0] for w in self.dictionary.search(word)] # strip point value
        cross_mode = mode.opposite()
        updated_squares = grid.get_word_squares(square, mode)

        # remove any words that would cause a contradiction later
        for i, s in enumerate(updated_squares):
            if not grid.is_empty(s):
                continue # skip squares that are already filled in

            cross_index = grid.get_word_squares(s, cross_mode).index(s)
            cross_word = grid.get_word(s, cross_mode)
            letters = self.dictionary.get_allowed_letters(cross_word, cross_index)
            words = [w for w in words if w[i] in letters]

        return words

    def get_next_target(self, grid):
        """
        Determines where to search next. Weighted combination that favors long words
        and words with fewer letters remaining
        """
        square = None
        mode = None
        max_score = -1

        for i in range(grid.size):
            for j in range(grid.size):
                if grid.is_empty((i, j)):
                    for m in [Mode.ACROSS, Mode.DOWN]:
                        temp_square = (i, j)
                        word = grid.get_word(temp_square, m)
                        score = len(word) + 5 * len(word.replace(' ',''))
                        if score > max_score:
                            square = temp_square
                            mode = m
                            max_score = score

        return square, mode

    def set_word(self, grid, square, mode, word):
        """Fills the given square with the given word
        todo see if it's possible to only use squares that are the start of a clue
        """
        word = word.upper()
        squares = grid.get_word_squares(square, mode)
        for i, square in enumerate(squares):
            if grid.get_square(square) != word[i]:
                grid.set_square(square, word[i])

    def search(self, grid):
        """ Recursive function that picks a square then loops through all available words.
        Returns false if no words are valid, true if the puzzle is complete"
        """
        self.nodes_searched += 1
        if self.nodes_searched % 1000 == 0:
            print(f"{self.nodes_searched} nodes searched")
            grid.print()
            print("")

        original_squares = deepcopy(grid.squares)
        square, mode = self.get_next_target(grid)

        if square == None:
            return True # no more words to search

        for word in self.get_possible_words(grid, square, mode):
            grid.squares = deepcopy(original_squares) #todo this will be slow
            result = self.set_word(grid, square, mode, word)
            if result == False:
                # word caused a contradiction, keep going to next word
                continue
            result = self.search(grid)
            if result == True:
                return True

        return False

