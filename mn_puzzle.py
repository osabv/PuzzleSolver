from puzzle import Puzzle
import math


class MNPuzzle(Puzzle):
    """
    An nxm puzzle, like the 15-puzzle, which may be solved, unsolved,
    or even unsolvable.
    """

    def __init__(self, from_grid, to_grid):
        """
        MNPuzzle in state from_grid, working towards
        state to_grid
        """
        # represent grid symbols with letters or numerals
        # represent the empty space with a "*"
        assert len(from_grid) > 0
        assert all([len(r) == len(from_grid[0]) for r in from_grid])
        assert all([len(r) == len(to_grid[0]) for r in to_grid])
        self.n, self.m = len(from_grid), len(from_grid[0])
        self.from_grid, self.to_grid = from_grid, to_grid


    def __eq__(self, other):
        """
        Return True if self equals other, and false otherwise.

        @rtype: bool
        """
        return type(self) == type(other) and self.from_grid == other.from_grid\
               and self.to_grid == other.to_grid

    def __str__(self):
        """
        Return a string representation.

        @rtype: str
        """
        current = ""
        solution = ""
        for row in self.from_grid:
            for cell in row:
                current += cell
            current += "\n"
        for row in self.to_grid:
            for cell in row:
                solution += cell
            solution += "\n"

        return ("Current configuration: \n{}Solution configuration: \n{}"
                .format(current, solution.strip()))

    def __repr__(self):
        """
        Return a simple string representation for the from_grid of a MNPuzzle

        @rtype: str
        """
        r = ""
        for row in self.from_grid:
            for cell in row:
                r += cell
            r += "\n"
        return r.strip()

    # legal extensions are configurations that can be reached by swapping one
    # symbol to the left, right, above, or below "*" with "*"

    def extensions(self):
        """
        Return a list of legal extensions of MNPuzzle self.

        @type self: MNPuzzle
        @rtype: list[MNPuzzle]
        """
        legal = []
        copy = MNPuzzle(self.from_grid, self.to_grid)
        pos_space = position(self, '*')
        row = pos_space[0]-1
        column = pos_space[1]-1

        if row-1 >= 0:
            pos_cell = position(self, self.from_grid[row-1][column])
            copy = switch_cells(self, pos_cell, pos_space)
            legal.append(copy)
            copy = MNPuzzle(self.from_grid, self.to_grid)
        if row+1 < self.n:
            pos_cell = position(self, self.from_grid[row+1][column])
            copy = switch_cells(self, pos_cell, pos_space)
            legal.append(copy)
            copy = MNPuzzle(self.from_grid, self.to_grid)
        if column-1 >= 0:
            pos_cell = position(self, self.from_grid[row][column-1])
            copy = switch_cells(self, pos_cell, pos_space)
            legal.append(copy)
            copy = MNPuzzle(self.from_grid, self.to_grid)
        if column+1 < self.m:
            pos_cell = position(self, self.from_grid[row][column+1])
            copy = switch_cells(self, pos_cell, pos_space)
            legal.append(copy)
            copy = MNPuzzle(self.from_grid, self.to_grid)

        return legal

    # TODO
    # override is_solved
    # a configuration is solved when from_grid is the same as to_grid

    def is_solved(self):
        """
        Return True iff Puzzle self is solved.

        @type self: MNPuzzle
        @rtype: bool
        """
        return self.from_grid == self.to_grid


# helper function
def position(puzzle, cell):
    """
    Return a list of two numbers indicating the location of a cell

    Precondition: cell is in the puzzle

    @type puzzle : MNPuzzle
    @type cell: string
    @rtype: list[row, column]
    """
    row = 0
    col = 0
    for r in puzzle.from_grid:
        row += 1
        for c in r:
            col += 1
            if c == cell:
                return [row, col-puzzle.m*(row-1)]


def switch_cells(puzzle, c1, c2):
    """
    Return a MNPuzzles with 2 of its cells switched

    @type puzzle: MNPuzzle
    @type p1: list
    @type p2: list
    @rtype: MNPuzzle
    """
    p = [list(x) for x in puzzle.from_grid]

    p[c1[0]-1][c1[1]-1], p[c2[0]-1][c2[1]-1] =\
        p[c2[0]-1][c2[1]-1], p[c1[0]-1][c1[1]-1]

    p = tuple(tuple(x) for x in p)

    new_puzzle = MNPuzzle(p, puzzle.to_grid)

    return new_puzzle


if __name__ == "__main__":
    target_grid = (("1", "2", "3"), ("4", "5", "*"))
    start_grid = (("*", "2", "3"), ("1", "4", "5"))
    from puzzle_tools import breadth_first_solve, depth_first_solve
    from time import time
    start = time()
    solution = breadth_first_solve(MNPuzzle(start_grid, target_grid))
    end = time()
    print("BFS solved: \n\n{} \n\nin {} seconds".format(
        solution, end - start))
    start = time()
    solution = depth_first_solve((MNPuzzle(start_grid, target_grid)))
    end = time()
    print("DFS solved: \n\n{} \n\nin {} seconds".format(
        solution, end - start))
