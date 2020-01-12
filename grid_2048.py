import numpy as np
from Move import EMove
import math


class Grid2048:
    """
    2048 game board. Contains methods for moving the grid left, right, up and down.
    """

    def __init__(self, grid):
        """
        Constructor, creates a new grid object.
        """
        self.grid = grid

    def clone(self):
        return Grid2048(grid=self.grid.copy())

    def insert(self, x, y, val):
        self.grid[x][y] = val

    def can_move(self, move):
        G = self.clone()

        if move == EMove.LEFT:
            G.move_left()
        if move == EMove.RIGHT:
            G.move_right()
        if move == EMove.DOWN:
            G.move_down()
        if move == EMove.UP:
            G.move_up()

        checks = [1 for i in range(4) for j in range(4) if G.grid[i][j] != self.grid[i][j]]
        return len(checks) > 0

    def move_dir(self, dir):
        if dir == EMove.LEFT:
            self.move_left()
        elif dir == EMove.UP:
            self.move_up()
        elif dir == EMove.DOWN:
            self.move_down()
        elif dir == EMove.RIGHT:
            self.move_right()

    def move(self, row):
        """
        Moves the entries in the row so adjacent numbers of power of 2 adds up.
        Returns a new row and the score.
        """
        row1 = list(filter(lambda a: a != 0, row))
        row1.append(1)
        row2 = []

        score_to_add = 0

        while len(row1) > 1:
            a = row1.pop(0)

            if row1[0] == a:
                row2.append(2 * a)
                row1.pop(0)
                score_to_add += 2 * a

            else:
                row2.append(a)

        for i in range(4 - len(row2)):
            row2.append(0)

        return row2, score_to_add

    def move_rev(self, row):
        """
        Reverses the row and moves the entries like move.
        Returns the a new row and the score.
        """
        row2, score = self.move(row[::-1])
        return row2[::-1], score

    def move_left(self):
        """
        Moves all rows in the grid to left.
        Returns the score to collect if this move is chosen.
        """
        grid2 = []
        score_to_collect = 0

        for row in self.grid:
            row2, sc = self.move(row)
            grid2.append(row2)
            score_to_collect += sc

        self.grid = grid2
        return score_to_collect

    def move_right(self):
        """
        Moves all rows in the grid to right.
        Returns the score to collect if this move is chosen.
        """
        grid2 = []
        score_to_collect = 0

        for row in self.grid:
            row2, sc = self.move_rev(row)
            grid2.append(row2)
            score_to_collect += sc

        self.grid = grid2
        return score_to_collect

    def transpose(self):
        """
        Transposes the grid like a matrix.
        """
        col0 = [item[0] for item in self.grid]
        col1 = [item[1] for item in self.grid]
        col2 = [item[2] for item in self.grid]
        col3 = [item[3] for item in self.grid]

        grid_T = [col0, col1, col2, col3]
        self.grid = grid_T

    def move_up(self):
        """
        EMoves the entries in the grid up.
        Returns the score to collect if this move is chosen.
        """
        self.transpose()

        grid2 = []
        score_to_collect = 0

        for row in self.grid:
            row2, score = self.move(row)
            grid2.append(row2)
            score_to_collect += score

        self.grid = grid2
        self.transpose()
        return score_to_collect

    def move_down(self):
        """
        Moves the entries in the grid down.
        Returns the score to collect if this move is chosen.
        """
        self.transpose()

        grid2 = []
        score_to_collect = 0

        for row in self.grid:
            row2, score = self.move_rev(row)
            grid2.append(row2)
            score_to_collect += score

        self.grid = grid2
        self.transpose()
        return score_to_collect

    def get_empty_cells(self):
        return [(i, j) for i in range(4) for j in range(4) if self.grid[i][j] == 0]

    def has_won(self):
        return True in [True for i in range(4) for j in range(4) if self.grid[i][j] >= 2048]

    @staticmethod
    def __cell_score(v):
        if v <= 0:
            return 0

        n = int(math.log(v, 2))
        return v * (n - 1)

    def compute_score(self):
        return sum([Grid2048.__cell_score(self.grid[i][j]) for i in range(4) for j in range(4)])
