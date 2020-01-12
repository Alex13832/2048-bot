import math

from Move import EMove


class Grid2048:
    """
    2048 game board. Contains methods for moving the grid left, right, up and down.
    """

    def __init__(self, grid=None):
        if grid is None:
            grid = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

        self.grid = grid

    def clone(self):
        return Grid2048(grid=self.grid.copy())

    def insert(self, x, y, val):
        self.grid[x][y] = val

    def can_move(self, direction):
        G = self.clone()

        if direction == EMove.LEFT:
            G.__move_left()
        if direction == EMove.RIGHT:
            G.__move_right()
        if direction == EMove.DOWN:
            G.move_down()
        if direction == EMove.UP:
            G.__move_up()

        checks = [1 for i in range(4) for j in range(4) if G.grid[i][j] != self.grid[i][j]]
        return len(checks) > 0

    def move_dir(self, direction):
        if direction == EMove.LEFT:
            self.__move_left()
        elif direction == EMove.UP:
            self.__move_up()
        elif direction == EMove.DOWN:
            self.move_down()
        elif direction == EMove.RIGHT:
            self.__move_right()

    def __move_left(self):
        self.grid = [self.__move(row) for row in self.grid]

    def __move_right(self):
        self.grid = [self.__move_rev(row) for row in self.grid]

    def __move_up(self):
        self.__transpose()
        self.grid = [self.__move(row) for row in self.grid]
        self.__transpose()

    def move_down(self):
        self.__transpose()
        self.grid = [self.__move_rev(row) for row in self.grid]
        self.__transpose()

    def __move(self, row):
        row1 = list(filter(lambda a: a != 0, row))
        row1.append(1)
        row2 = []

        while len(row1) > 1:
            a = row1.pop(0)

            if row1[0] == a:
                row2.append(2 * a)
                row1.pop(0)
            else:
                row2.append(a)

        return row2 + ([0] * (4 - len(row2)))

    def __move_rev(self, row):
        row2 = self.__move(row[::-1])
        return row2[::-1]

    def __transpose(self):
        col0 = [item[0] for item in self.grid]
        col1 = [item[1] for item in self.grid]
        col2 = [item[2] for item in self.grid]
        col3 = [item[3] for item in self.grid]
        self.grid = [col0, col1, col2, col3]

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
