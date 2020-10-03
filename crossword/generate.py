from copy import deepcopy

from crossword.dictionary import CrosswordDictionary
from crossword.grid import Grid, Mode

class Generator:

    def __init__(self, dictionary):
        self.dictionary = dictionary
        self.nodes_searched = 0
        self.used_words = []
        self.unfilled_words = []
        self.score = 0
        self.target_score = 0

    def get_possible_words(self, grid, square, mode):
        """ Returns a list of all possible words for a given square and direction
            sorted from best to worst
        """
        word = grid.get_word(square, mode)
        words = self.dictionary.search(word)
        cross_mode = mode.opposite()
        updated_squares = grid.get_word_squares(square, mode)

        # remove any words that would cause a contradiction later
        for i, s in enumerate(updated_squares):
            if not grid.is_empty(s):
                continue # skip squares that are already filled in

            cross_index = grid.get_word_squares(s, cross_mode).index(s)
            cross_word = grid.get_word(s, cross_mode)
            letters = self.dictionary.get_allowed_letters(cross_word, cross_index)
            words = [w for w in words if w[0][i] in letters]

        return [(w[0], int(w[1])) for w in words]

    def get_next_target(self, grid):
        """
        Determines where to search next. Weighted combination that favors long words
        and words with fewer letters remaining
        """
        square = None
        mode = None
        max_score = -1

        for s, m in self.unfilled_words:
            word = grid.get_word(s, m)
            if ' ' not in word:
                # this word has been filled by other words
                # return it immediately to update the used_words list and total score
                return s, m

            score = len(word) + 5 * len(word.replace(' ',''))
            if score > max_score:
                 square = s
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

    def optimize(self, grid, target_score=None):
        self.nodes_searched = 0
        self.words_used = []
        self.unfilled_words = []
        self.score = 0
        self.target_score = target_score

        for square, mode in grid.get_all_words():
            word = grid.get_word(square, mode)
            if ' ' in word:
                self.unfilled_words.append((square, mode))
            else:
                self.words_used.append(word)
                self.score += int(self.dictionary.search(word)[0][1])


        return self.search(grid)

    def search(self, grid):
        """ Recursive function that picks a square then loops through all available words.
        Returns false if no words are valid, true if the puzzle is complete"
        """
        self.nodes_searched += 1
        if self.nodes_searched % 10 == 0:
            print(f"{self.nodes_searched} nodes searched")
            print(f"Score:{self.score}")
            grid.print()
            print("")

        original_squares = deepcopy(grid.squares)
        square, mode = self.get_next_target(grid)

        if square == None:
            if self.target_score is None:
                self.target_score = self.score - 1
            return self.score # no more words to search

        self.unfilled_words.remove((square, mode))

        for word, word_score in self.get_possible_words(grid, square, mode):
            maximum_score = self.score + word_score + 55 * len(self.unfilled_words)
            if self.target_score and maximum_score < self.target_score:
                continue

            if word in self.used_words:
                continue

            self.used_words.append(word)
            self.score += word_score

            grid.squares = deepcopy(original_squares) #todo this will be slow
            self.set_word(grid, square, mode, word)
            new_score = self.search(grid)

            if self.target_score and new_score >= self.target_score:
                return new_score

            self.used_words.pop()
            self.score -= word_score

        self.unfilled_words.append((square, mode))

        return self.score

