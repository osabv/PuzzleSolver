from puzzle import Puzzle


class GridPegSolitairePuzzle(Puzzle):
    """
    Snapshot of peg solitaire on a rectangular grid. May be solved,
    unsolved, or even unsolvable.
    """

    def __init__(self, marker, marker_set):
        """
        Create a new GridPegSolitairePuzzle self with
        marker indicating pegs, spaces, and unused
        and marker_set indicating allowed markers.

        @type marker: list[list[str]]
        @type marker_set: set[str]
                          "#" for unused, "*" for peg, "." for empty
        """
        assert isinstance(marker, list)
        assert len(marker) > 0
        assert all([len(x) == len(marker[0]) for x in marker[1:]])
        assert all([all(x in marker_set for x in row) for row in marker])
        assert all([x == "*" or x == "." or x == "#" for x in marker_set])
        self._marker, self._marker_set = marker, marker_set

    def __eq__(self, other):
        """
        @type self: GridPegSolitairePuzzle
        @type other: GridPegSolitairePuzzle | Any
        @rtype: bool

        Return whether GridPegSolitairePuzzle self is equivalent to other.
        """
        return (type(other) == type(self) and
                self._marker == other._marker and
                self._marker_set == other._marker_set)

    def __str__(self):
        """
        Return a string representation.

        @rtype: str
        """
        width = len(self._marker[0])
        height = len(self._marker)

        string = ''

        for row in self._marker:
            for obj in row:
                string += obj
            string += '\n'

        return ("Current marker: \n{}".format(string.strip()))

    # legal extensions consist of all configurations that can be reached by
    # making a single jump from this configuration-

    def extensions(self):
        """
        Return list of extensions of SudokuPuzzle self.

        @type self: GridPegSolitairePuzzle
        @rtype: list[GridPegSolitairePuzzle]
        """
        width = len(self._marker[0])
        height = len(self._marker)
        list_of_exten = []

        list_coord = []
        if len(self._marker) != 0:
            for n in range(height):
                if '.' in self._marker[n]:
                    row = n
                    col = self._marker[n].index('.')
                    list_coord.append((row, col))

        for coord in list_coord:
            x = coord[0]
            y = coord[1]

            # check top
            if x - 2 >= 0:
                if self._marker[x-2][y] == '*' and self._marker[x-1][y] == '*':
                    new_board = make_top_board(self._marker, x, y)
                    copy = GridPegSolitairePuzzle(new_board, self._marker_set)
                    list_of_exten.append(copy)
            # check right
            if y + 2 < width:
                if self._marker[x][y+2] == '*' and self._marker[x][y+1] == '*':
                    new_board = make_right_board(self._marker, x, y)
                    copy = GridPegSolitairePuzzle(new_board, self._marker_set)
                    list_of_exten.append(copy)
            # check bottom
            if x + 2 < height:
                if self._marker[x + 2][y] == '*' and self._marker[x + 1][y] == '*':
                    new_board = make_bottom_board(self._marker, x, y)
                    copy = GridPegSolitairePuzzle(new_board, self._marker_set)
                    list_of_exten.append(copy)
            # check left
            if y - 2 >= 0:
                if self._marker[x][y-2] == '*' and self._marker[x][y-1] == '*':
                    new_board = make_left_board(self._marker, x, y)
                    copy = GridPegSolitairePuzzle(new_board, self._marker_set)
                    list_of_exten.append(copy)

        return list_of_exten

    # A configuration is solved when there is exactly one "*" left
    def is_solved(self):
        """
        Return whether GridPegSolitairePuzzle self is solved.

        @type self: GridPegSolitairePuzzle
        @rtype: bool
        """
        counter = 0
        if not self._marker is None:
            for row in self._marker:
                for char in row:
                    if char == "*":
                        counter += 1

        return counter == 1

def make_top_board(board, x, y):
    """
    Return a new marker for an extension of GridPegSolitairePuzzle

    @type board: list[list[str]]
    @type x: int
    @type y: int
    @rtype: list[list[str]]
    """
    copy = []
    for row_num in range(len(board)):
        if row_num == x-2:
            copy_row = []
            for col_num in range(len(board[row_num])):
                if col_num == y:
                    copy_row.append('.')
                else:
                    copy_row.append(board[row_num][col_num])
            copy.append(copy_row)
        elif row_num == x-1:
            copy_row = []
            for col_num in range(len(board[row_num])):
                if col_num == y:
                    copy_row.append('.')
                else:
                    copy_row.append(board[row_num][col_num])
            copy.append(copy_row)
        elif row_num == x:
            copy_row = []
            for col_num in range(len(board[row_num])):
                if col_num == y:
                    copy_row.append('*')
                else:
                    copy_row.append(board[row_num][col_num])
            copy.append(copy_row)
        else:
            copy_row = []
            for col_num in range(len(board[row_num])):
                copy_row.append(board[row_num][col_num])
            copy.append(copy_row)
    return copy

def make_right_board(board, x, y):
    """
    Return a new marker for an extension of GridPegSolitairePuzzle

    @type board: list[list[str]]
    @type x: int
    @type y: int
    @rtype: list[list[str]]
    """
    copy = []
    for row_num in range(len(board)):
        if row_num == x:
            copy_row = []
            for col_num in range(len(board[row_num])):
                if col_num == y:
                    copy_row.append('*')
                elif col_num == y+1:
                    copy_row.append('.')
                elif col_num == y+2:
                    copy_row.append('.')
                else:
                    copy_row.append(board[row_num][col_num])
            copy.append(copy_row)
        else:
            copy_row = []
            for col_num in range(len(board[row_num])):
                copy_row.append(board[row_num][col_num])
            copy.append(copy_row)
    return copy

def make_bottom_board(board, x, y):
    """
    Return a new marker for an extension of GridPegSolitairePuzzle

    @type board: list[list[str]]
    @type x: int
    @type y: int
    @rtype: list[list[str]]
    """
    copy = []
    for row_num in range(len(board)):
        if row_num == x:
            copy_row = []
            for col_num in range(len(board[row_num])):
                if col_num == y:
                    copy_row.append('*')
                else:
                    copy_row.append(board[row_num][col_num])
            copy.append(copy_row)
        elif row_num == x+1:
            copy_row = []
            for col_num in range(len(board[row_num])):
                if col_num == y:
                    copy_row.append('.')
                else:
                    copy_row.append(board[row_num][col_num])
            copy.append(copy_row)
        elif row_num == x+2:
            copy_row = []
            for col_num in range(len(board[row_num])):
                if col_num == y:
                    copy_row.append('.')
                else:
                    copy_row.append(board[row_num][col_num])
            copy.append(copy_row)
        else:
            copy_row = []
            for col_num in range(len(board[row_num])):
                copy_row.append(board[row_num][col_num])
            copy.append(copy_row)
    return copy

def make_left_board(board, x, y):
    """
    Return a new marker for an extension of GridPegSolitairePuzzle

    @type board: list[list[str]]
    @type x: int
    @type y: int
    @rtype: list[list[str]]
    """
    copy = []
    for row_num in range(len(board)):
        if row_num == x:
            copy_row = []
            for col_num in range(len(board[row_num])):
                if col_num == y-2:
                    copy_row.append('.')
                elif col_num == y-1:
                    copy_row.append('.')
                elif col_num == y:
                    copy_row.append('*')
                else:
                    copy_row.append(board[row_num][col_num])
            copy.append(copy_row)
        else:
            copy_row = []
            for col_num in range(len(board[row_num])):
                copy_row.append(board[row_num][col_num])
            copy.append(copy_row)
    return copy

if __name__ == "__main__":
    from puzzle_tools import depth_first_solve

    grid = [["*", "*", "*", "*", "*"],
            ["*", "*", "*", "*", "*"],
            ["*", "*", "*", "*", "*"],
            ["*", "*", ".", "*", "*"],
            ["*", "*", "*", "*", "*"]]
    gpsp = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
    import time

    start = time.time()
    solution = depth_first_solve(gpsp)
    end = time.time()
    print("Solved 5x5 peg solitaire in {} seconds.".format(end - start))
    print("Using depth-first: \n{}".format(solution))
