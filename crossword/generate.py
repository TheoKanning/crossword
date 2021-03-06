from copy import deepcopy
import time

from crossword.grid import Grid

class SearchInfo:

    def __init__(self,
            unfilled_words,
            used_words,
            end_time=0,
            score=0,
            target_score=None,
            verbose=False):
        self.end_time=end_time
        self.nodes_searched = 0
        self.unfilled_words = unfilled_words
        self.used_words = used_words
        self.score = score
        self.target_score = target_score
        self.verbose = verbose

class Generator:

    def __init__(self, dictionary, verbose=False):
        self.dictionary = dictionary

    def optimize(self, original_grid, target_score=None, search_time=100, verbose=False):
        grid = Grid(deepcopy(original_grid.squares))
        info = SearchInfo(
                unfilled_words=[],
                used_words=[],
                end_time=100,
                score=0,
                target_score=target_score,
                verbose=verbose)

        for square, mode in grid.get_all_words():
            word = grid.get_word(square, mode)
            if ' ' in word:
                info.unfilled_words.append((square, mode))
            else:
                info.used_words.append(word)
                info.score += int(self.dictionary.search(word)[0][1])

        return self.search(grid, info)

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
                continue  # skip squares that are already filled in

            cross_index = grid.get_word_squares(s, cross_mode).index(s)
            cross_word = grid.get_word(s, cross_mode)
            letters = self.dictionary.get_allowed_letters(cross_word, cross_index)
            words = [w for w in words if w[0][i] in letters]

        return [(w[0], int(w[1])) for w in words]

    def get_next_target(self, grid, info):
        """
        Determines where to search next. Sorts by length and letters filled in, then resorts
        top 10 and picks the word with the fewest remaining possibilities.
        """

        def score(target):
            square, mode = target
            word = grid.get_word(square, mode)
            return len(word) + 5 * len(word.replace(' ', ''))

        def number_of_options(target):
            square, mode = target
            word = grid.get_word(square, mode)
            return len(self.dictionary.search(word))

        # re-order top 10 based on how many possibilities they have remaining, fewer first
        info.unfilled_words.sort(reverse=True, key=score)
        info.unfilled_words[0:10] = sorted(info.unfilled_words[0:10], key=number_of_options)

        return info.unfilled_words[0]

    def set_word(self, grid, square, mode, word):
        """Fills the given square with the given word
        """
        word = word.upper()
        squares = grid.get_word_squares(square, mode)
        for i, square in enumerate(squares):
            if grid.get_square(square) != word[i]:
                grid.set_square(square, word[i])

    def search(self, grid, info):
        """ Recursive function that picks a square then loops through all available words.
        Returns false if no words are valid, true if the puzzle is complete"
        """
        info.nodes_searched += 1
        if info.verbose and info.nodes_searched % 10 == 0:
            print(f"{info.nodes_searched} nodes searched")
            print(f"Score:{info.score}")
            grid.print()
            print("")

        if not info.unfilled_words:
            if info.target_score is None:
                info.target_score = info.score - 1
            return grid, info.score  # no more words to search

        original_squares = deepcopy(grid.squares)
        square, mode = self.get_next_target(grid, info)

        info.unfilled_words.remove((square, mode))

        for word, word_score in self.get_possible_words(grid, square, mode):
            maximum_score = info.score + word_score + 55 * len(info.unfilled_words)
            if info.target_score and maximum_score < info.target_score:
                continue

            if word in info.used_words:
                continue

            info.used_words.append(word)
            info.score += word_score

            grid.squares = deepcopy(original_squares)
            self.set_word(grid, square, mode, word)
            grid, new_score = self.search(grid, info)

            if info.target_score and new_score >= info.target_score:
                return grid, new_score

            info.used_words.pop()
            info.score -= word_score

        info.unfilled_words.append((square, mode))

        return grid, info.score
