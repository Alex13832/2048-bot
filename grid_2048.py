import math

from move import EMove


class Grid2048:
    """
    2048 game board. Contains methods for moving the grid left, right, up and down.
    """

    def __init__(self, grid=None):
        if grid is None:
            grid = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.grid = grid
        self.last_score = 0
        self.moved = None

    def clone(self):
        """
        Clones this grid.
        :return:
        """
        return Grid2048(grid=self.grid.copy())

    def insert(self, x, y, val):
        """
        Inserts a value in the grid.
        :param x: x-pos
        :param y: y-pos
        :param val: value to insert.
        :return:
        """
        self.grid[x][y] = val

    def can_move(self, move):
        """
        Computes if the grid can be moved in the desired input direction.
        :param move: desired direction.
        :return: if the grid can be moved.
        """
        game = self.clone()

        if move == EMove.LEFT:
            game.move_left()
        if move == EMove.RIGHT:
            game.move_right()
        if move == EMove.DOWN:
            game.move_down()
        if move == EMove.UP:
            game.move_up()

        can_move = [True for x in range(4) for y in range(4) if game.grid[x][y] != self.grid[x][y]]

        return len(can_move) > 0

    def move_dir(self, direction):
        """
        Moves the grid in the desired direction.
        :param direction: direction.
        :return:
        """
        if direction == EMove.LEFT:
            self.move_left()
        elif direction == EMove.UP:
            self.move_up()
        elif direction == EMove.DOWN:
            self.move_down()
        elif direction == EMove.RIGHT:
            self.move_right()

    @staticmethod
    def move(row):
        """
        Moves the entries in the row so adjacent numbers of power of 2 adds up.
        Returns a new row and the score.
        :param row: row to move.
        :return:
        """
        # row1 = list(filter(lambda a: a != 0, row))
        row1 = [x for x in row if x != 0]
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
        self.last_score = score_to_collect
        self.moved = EMove.LEFT

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
        self.last_score = score_to_collect
        self.moved = EMove.RIGHT

        return score_to_collect

    def transpose(self):
        """
        Transposes the grid like a matrix.
        """
        col0 = [item[0] for item in self.grid]
        col1 = [item[1] for item in self.grid]
        col2 = [item[2] for item in self.grid]
        col3 = [item[3] for item in self.grid]

        self.grid = [col0, col1, col2, col3]

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
        self.last_score = score_to_collect
        self.moved = EMove.UP

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
        self.last_score = score_to_collect
        self.moved = EMove.DOWN

        return score_to_collect

    def get_empty_cells(self):
        """
        Returns the empty cells in the grid.
        :return:
        """
        return [(i, j) for i in range(4) for j in range(4) if self.grid[i][j] == 0]

    def has_won(self):
        """
        Finds if the game has reached 2048 or higher.
        :return:
        """
        return 2048 in [2048 for i in range(4) for j in range(4) if self.grid[i][j] >= 2048]

    @property
    def compute_score(self):
        """
        Computes the current score.
        :return:
        """
        values = [self.grid[i][j] for i in range(4) for j in range(4)]
        scores = [value * (math.log(value, 2) - 1) for value in values if value > 0]
        return sum(scores)
