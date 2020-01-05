import numpy as np
from Move import EMove

class Grid2048:
    """
    2048 game board. Contains methods for moving the grid left, right, up and down.
    """

    def __init__(self, grid=[[0,0,0,0],
                             [0,0,0,0],
                             [0,0,0,0],
                             [0,0,0,0]]):
        """
        Constructor, creates a new grid object.
        """
        self.grid = grid
        self.lastScore = 0
        self.moved = None


    def clone(self):
        grid=[[0,0,0,0],
             [0,0,0,0],
             [0,0,0,0],
             [0,0,0,0]]

        for i in range(4):
            for j in range(4):
                grid[i][j] = self.grid[i][j]

        G = Grid2048(grid=grid)

        return G


    def insert(self, x, y, val):
        self.grid[x][y] = val


    def can_move(self, move):
        G = Grid2048(grid=[[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]])
        for i in range(4):
            for j in range(4):
                G.grid[i][j] = self.grid[i][j]

        score = 0
        if move == EMove.LEFT:
            score = G.move_left(put_rand=False)
        if move == EMove.RIGHT:
            score = G.move_right(put_rand=False)
        if move == EMove.DOWN:
            score = G.move_down(put_rand=False)
        if move == EMove.UP:
            score = G.move_up(put_rand=False)

        canMove = False

        for i in range(4):
            for j in range(4):
                if G.grid[i][j] != self.grid[i][j]:
                    canMove = True
                    break

        return canMove


    def move(self, row):
        """
        Moves the entries in the row so adjacent numbers of power of 2 adds up.
        Returns a new row and the score.
        """
        score = 0

        row1 = list(filter(lambda a: a != 0, row))
        row1.append(1)
        row2 = []

        score_to_add = 0

        while len(row1) > 1:
            a = row1.pop(0)

            if row1[0] == a:
                row2.append(2*a)
                row1.pop(0)
                score_to_add += 2*a

            else:
                row2.append(a)

        for i in range(4-len(row2)):
            row2.append(0)

        return row2, score_to_add


    def move_rev(self, row):
        """
        Reverses the row and moves the entries like move.
        Returns the a new row and the score.
        """
        row2, score = self.move(row[::-1])
        return row2[::-1], score


    def move_left(self, put_rand=True):
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
        self.lastScore = score_to_collect
        self.moved = EMove.LEFT
        if put_rand:
            self.insert_random_2_or_4()

        return score_to_collect


    def move_right(self, put_rand=True):
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
        self.lastScore = score_to_collect
        self.moved = EMove.RIGHT
        if put_rand:
            self.insert_random_2_or_4()

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


    def move_up(self, put_rand=True):
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
        self.lastScore = score_to_collect
        self.moved = EMove.UP
        if put_rand:
            self.insert_random_2_or_4()

        return score_to_collect


    def move_down(self, put_rand=True):
        """
        Moves the entris in the grid down.
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
        self.lastScore = score_to_collect
        self.moved = EMove.DOWN
        if put_rand:
            self.insert_random_2_or_4()

        return score_to_collect


    def largest_in_upper_left_corner(self):
        corner = self.grid[0][0]

        for i in range(4):
            for j in range(4):
                if i != 0 and j != 0:
                    if self.grid[i][j] >= corner:
                        return False

        return True


    def insert_random_2_or_4(self):
        """
        Inserts a random 2 or 4 at a random position (i,j) in the grid if grid(i,j) = 0.
        The probability of getting a 4 is 0.1.
        """
        rand_val = np.random.rand()
        rand = 2

        if rand_val <= 0.1:
            rand = 4

        flag = True

        count_row_with_zeros = 0
        for row in self.grid:
            if 0 in row:
                count_row_with_zeros += 1

        if count_row_with_zeros > 0:
            flag = False

        while not flag:
            rand_x = np.random.randint(0,4)
            rand_y = np.random.randint(0,4)

            if self.grid[rand_x][rand_y] == 0:
                self.grid[rand_x][rand_y] = rand
                flag = True


    def empty_cells(self):
        """
        Returns the number of empty cells in a grid.
        """
        score = 0

        for row in self.grid:
            for cell in row:
                if cell == 0:
                    score += 1

        return score


    def largest_in_lower_left_score(self):
        corner = self.grid[3][0]
        score = 20

        for i in range(4):
            for j in range(4):
                if i != 3 and j != 0 and self.grid[i][j] > corner:
                    score -= 10

        return score


    def smoothness_score(self):
        score = 0
        GL = self.clone()
        GD = self.clone()

        GL.move_right(put_rand=False)
        GD.move_up(put_rand=False)

        for i in range(4):
            for j in range(4):

                if GL.grid[i][j] == 0 and self.grid[i][j] != 0:
                    score += 1

                if GD.grid[i][j] == 0 and self.grid[i][j] != 0:
                    score += 1

        return score


    def smoothness_horizontally(self):
        score = 0

        for row in self.grid:
            a,b,c,d = row[0], row[1], row[2], row[3]
            if a == b:
                score += 1
                if b == c:
                    score += 1
                    if c == d:
                        score += 1


        return score




    def number_of_values(self):
        values = dict()

        for i in range(4):
            for j in range(4):
                values[self.grid[i][j]] = 1

        score = 0

        for key in values:
            score += 1

        return score


    def unique_score(self):
        score = 0

        for row in self.grid:
            unique = list(set(row))
            score += (4 - len(unique))

        self.transpose()

        for row in self.grid:
            unique = list(set(row))
            score += (4 - len(unique))

        self.transpose()

        return score


    def number_of_2s_and_4s(self):
        score = 0

        for row in self.grid:
            for x in row:
                if x == 2 :
                    score += 1
                if x == 4:
                    score += 1
                if x == 8:
                    score += 1

        return score


    def monotonic_score(self):
        """
        Calculates a score related to the matrix' monotocity.
        """
        score = 0

        G1 = self.clone()
        G1.grid = list(reversed(G1.grid))

        for row in G1.grid:
            a,b,c,d = row[0], row[1], row[2], row[3]

            if a > b:
                score += 1
                if b > c:
                    score += 1
                    if c > d:
                        score += 1

        G2 = self.clone()
        G2.transpose()

        for row in G2.grid:
            a,b,c,d = row[3], row[2], row[1], row[0]

            if a > b:
                score += 1
                if b > c:
                    score += 1
                    if c > d:
                        score += 1


        return score


    def max_value(self):
        max_val = 0

        for row in self.grid:
            if max_val > max(row):
                max_val = max(row)

        return max_val



    def get_empty_cells(self):

        empty_cells = []

        for i in range(4):
            for j in range(4):

                if self.grid[i][j] == 0:

                    empty_cells.append((i,j))

        return empty_cells


    def has_won(self):
        score = 0
        for row in self.grid:
            for x in row:
                if x >= 2048:
                    return True

        return False


    def is_terminated(self):

        if self.has_won():
            return True

        score = -1

        if self.empty_cells() == 0:
            score  = 0
            G = self.clone()
            G.move_right()
            score += G.lastScore
            G.move_left()
            score += G.lastScore
            G.move_up()
            score += G.lastScore
            G.move_down()
            score += G.lastScore

        return score == 0


    def clustering_score(self):
        clust_score = 0
        G = self.grid
        neighbors = [-1, 0, 1]

        for i in range(4):
            for j in range(4):
                if G[i][j] == 0:
                    continue

                numberOfNeighbors = 0
                nsum = 0

                for nx in neighbors:
                    x = i + nx

                    if x < 0 or x > 3:
                        continue

                    for ny in neighbors:
                        y = ny + j

                        if y < 0 or y > 3:
                            continue

                        if G[i][j] > 0:
                            numberOfNeighbors += 1
                            nsum += abs(G[i][j] - G[x][y])

                clust_score += nsum/numberOfNeighbors


        return clust_score
