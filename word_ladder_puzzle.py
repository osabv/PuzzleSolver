from puzzle import Puzzle

seen_words = set()

class WordLadderPuzzle(Puzzle):
    """
    A word-ladder puzzle that may be solved, unsolved, or even unsolvable.
    """

    def __init__(self, from_word, to_word, ws):
        """
        Create a new word-ladder puzzle with the aim of stepping
        from from_word to to_word using words in ws, changing one
        character at each step.

        @type from_word: str
        @type to_word: str
        @type ws: set[str]
        @rtype: None
        """
        (self._from_word, self._to_word, self._word_set) = (from_word,
                                                            to_word, ws)
        # set of characters to use for 1-character changes
        self._chars = "abcdefghijklmnopqrstuvwxyz"

    def __str__(self):
        """
        Return a human-readable string representation of WordLadderPuzzle self.

        @type self: WordLadderPuzzle
        @rtype from_word: str
        @rtype to_word: str
        @rtype ws: list[str]
        """
        return "from_word: '{}' \nto_word: '{}'".format(
            self._from_word, self._to_word)

    def __eq__(self, other):
        """
        Return whether WordLadderPuzzle self is equivalent to other.

        @type self: WordLadderPuzzle
        @type other: WordLadderPuzzle
        @rtype: bool
        """
        return (self._from_word == other._from_word and
                self._to_word == other._to_word and
                self._word_set == other._word_set) 
    
    def __repr__(self):
            """
            Return a human-readable string representation of WordLadderPuzzle 
            self that includes all information.
            
            @type self: WordLadderPuzzle
            @rtype from_word: str
            @rtype to_word: str
            @rtype ws: list[str]
            """        
            return "from_word: '{}' \nto_word: '{}' \nword_set: '{}'".format(
                self._from_word, self._to_word, self._word_set)   
    
    # this WordLadderPuzzle is solved when _from_word is the same as
    # _to_word  
    
    def is_solved(self):
        """
        Return whether WordLadderPuzzle self is solved.
        
        @type self: WordLadderPuzzle
        @rtype: bool
        True
        """
        return (self._from_word == self._to_word) and (self._from_word in
                                                       self._word_set and
                                                       self._to_word in
                                                       self._word_set)        
     
    # legal extensions are WordLadderPuzzles that have a from_word that can
    # be reached from this one by changing a single letter to one of those
    # in self._chars
    
    def extensions(self):
        """
        Return list of extensions of WordLadderPuzzle self.
        
        @type self: WordLadderPuzzle
        @rtype: list[WordLadderPuzzle]
        """
        lst_ext = []
        seen_words = set()
        seen_words.add(self._from_word)
        if not self.is_solved():
            for i in range(len(self._from_word)):
                for ch in self._chars:
                    if i == 0:
                        new_from_word = str(ch).lower() + self._from_word[1:]
                        if new_from_word in self._word_set and new_from_word\
                           != self._from_word and new_from_word not in\
                           seen_words:
                            temp = WordLadderPuzzle(new_from_word,
                                                    self._to_word,
                                                    self._word_set)
                            lst_ext.append(temp)
                            seen_words.add(new_from_word)
                    else:
                        new_from_word = self._from_word[:i] + str(ch).lower()\
                            + self._from_word[i+1:]
                        if new_from_word in self._word_set and new_from_word\
                           != self._from_word and new_from_word not in\
                           seen_words:
                            temp = WordLadderPuzzle(new_from_word,
                                                    self._to_word,
                                                    self._word_set)
                            lst_ext.append(temp)
                            seen_words.add(new_from_word)

        return lst_ext

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    from puzzle_tools import breadth_first_solve, depth_first_solve
    from time import time
    with open("words", "r", encoding = 'UTF-8') as words:
        word_set = set(words.read().split())
    w = WordLadderPuzzle("same", "cost", word_set)
    start = time()
    sol = breadth_first_solve(w)
    end = time()
    print("Solving word ladder from same->cost")
    print("...using breadth-first-search")
    print("Solutions: {} took {} seconds.".format(sol, end - start))
    start = time()
    sol = depth_first_solve(w)
    end = time()
    print("Solving word ladder from same->cost")
    print("...using depth-first-search")
    print("Solutions: {} took {} seconds.".format(sol, end - start))
