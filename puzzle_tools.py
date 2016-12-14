"""
Some functions for working with puzzles
"""
from puzzle import Puzzle
from collections import deque
# set higher recursion limit
# which is needed in PuzzleNode.__str__
# uncomment the next two lines on a unix platform, say CDF
# import resource
# resource.setrlimit(resource.RLIMIT_STACK, (2**29, -1))
import sys
sys.setrecursionlimit(10**6)


dfs_visited = set()
def depth_first_solve(puzzle):
    """
    Return a path from PuzzleNode(puzzle) to a PuzzleNode containing
    a solution, with each child containing an extension of the puzzle
    in its parent.  Return None if this is not possible.

    @type puzzle: Puzzle
    @rtype: PuzzleNode
    """
    global dfs_visited
    if str(puzzle) in dfs_visited:
        return None
    elif puzzle.is_solved():
        final = PuzzleNode(puzzle, [], None)
        dfs_visited.clear()
        return final
    else:
        dfs_visited.add(str(puzzle))
        children = puzzle.extensions()
        for child in children:
            next_recur = depth_first_solve(child)
            if next_recur is None:
                continue
            else:
                return PuzzleNode(puzzle, [next_recur], None)

bfs_visited = []
def breadth_first_solve(puzzle):
    """
    Return a path from PuzzleNode(puzzle) to a PuzzleNode containing
    a solution, with each child PuzzleNode containing an extension
    of the puzzle in its parent.  Return None if this is not possible.

    @type puzzle: Puzzle
    @rtype: PuzzleNode
    """
    global bfs_visited
    if puzzle in bfs_visited:
        return None
    elif puzzle.is_solved():
        final = PuzzleNode(puzzle, [], None)
        bfs_visited.clear()
        return final
    else:
        bfs_visited.append(puzzle)
        children = puzzle.extensions()
        for child in children:
            if child.is_solved():
                final = PuzzleNode(puzzle, [child], None)
                return final
            bfs_visited.append(child)
        for child in children:
            grandchildren = child.extensions()
            for grandchild in grandchildren:
                next_recur = breadth_first_solve(grandchild)
                if next_recur is None:
                    continue
                else:
                    return PuzzleNode(child, [next_recur], None)

# Class PuzzleNode helps build trees of PuzzleNodes that have
# an arbitrary number of children, and a parent.
class PuzzleNode:
    """
    A Puzzle configuration that refers to other configurations that it
    can be extended to.
    """

    def __init__(self, puzzle=None, children=None, parent=None):
        """
        Create a new puzzle node self with configuration puzzle.

        @type self: PuzzleNode
        @type puzzle: Puzzle | None
        @type children: list[PuzzleNode]
        @type parent: PuzzleNode | None
        @rtype: None
        """
        self.puzzle, self.parent = puzzle, parent
        if children is None:
            self.children = []
        else:
            self.children = children[:]

    def __eq__(self, other):
        """
        Return whether PuzzleNode self is equivalent to other

        @type self: PuzzleNode
        @type other: PuzzleNode | Any
        @rtype: bool
        """
        return (type(self) == type(other) and
                self.puzzle == other.puzzle and
                all([x in self.children for x in other.children]) and
                all([x in other.children for x in self.children]))

    def __str__(self):
        """
        Return a human-readable string representing PuzzleNode self.

        # doctest not feasible.
        """
        return "{}\n\n{}".format(self.puzzle,
                                 "\n".join([str(x) for x in self.children]))
