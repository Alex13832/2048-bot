import math
import random

from move import *
from grid_2048 import Grid2048


class Engine2048:

    def __init__(self):
        self.bestMove = EMove.LEFT
        self.linked_move = None
        self.actualScore = 0
        self.best_score = -math.inf

        w1 = [[1 << 15, 1 << 14, 1 << 13, 1 << 12],
              [1 << 8, 1 << 9, 1 << 10, 1 << 11],
              [1 << 7, 1 << 6, 1 << 5, 1 << 4],
              [1, 1 << 1, 1 << 2, 1 << 3]]

        w2 = [[1 << 12, 1 << 13, 1 << 14, 1 << 15],
              [1 << 11, 1 << 10, 1 << 9, 1 << 8],
              [1 << 4, 1 << 5, 1 << 6, 1 << 7],
              [1 << 3, 1 << 2, 1 << 1, 1]]

        w3 = [[1 << 3, 1 << 2, 1 << 1, 1],
              [1 << 4, 1 << 5, 1 << 6, 1 << 7],
              [1 << 11, 1 << 10, 1 << 9, 1 << 8],
              [1 << 12, 1 << 13, 1 << 14, 1 << 15]]

        w4 = [[1, 1 << 1, 1 << 2, 1 << 3],
              [1 << 7, 1 << 6, 1 << 5, 1 << 4],
              [1 << 8, 1 << 9, 1 << 10, 1 << 11],
              [1 << 15, 1 << 14, 1 << 13, 1 << 12]]

        w5 = [[1 << 15, 1 << 8, 1 << 7, 1],
              [1 << 14, 1 << 9, 1 << 6, 1 << 1],
              [1 << 13, 1 << 10, 1 << 5, 1 << 2],
              [1 << 12, 1 << 11, 1 << 4, 1 << 3]]

        w6 = [[1 << 12, 1 << 11, 1 << 4, 1 << 3],
              [1 << 13, 1 << 10, 1 << 5, 1 << 2],
              [1 << 14, 1 << 9, 1 << 6, 1 << 1],
              [1 << 15, 1 << 8, 1 << 7, 1]]

        w7 = [[1 << 3, 1 << 4, 1 << 11, 1 << 12],
              [1 << 2, 1 << 5, 1 << 10, 1 << 13],
              [1 << 1, 1 << 6, 1 << 9, 1 << 14],
              [1, 1 << 7, 1 << 8, 1 << 15]]

        w8 = [[1, 1 << 7, 1 << 8, 1 << 15],
              [1 << 1, 1 << 6, 1 << 9, 1 << 14],
              [1 << 2, 1 << 5, 1 << 10, 1 << 13],
              [1 << 3, 1 << 4, 1 << 11, 1 << 12]]

        self.weights = [w1, w2, w3, w4, w5, w6, w7, w8]

    def heuristic_score_weighted(self, grid: Grid2048):
        """
        Returns the heuristic score fot the input grid.
        """
        max_score = -math.inf
        for weights in self.weights:

            score = sum([weights[i][j] * grid.grid[i][j] for i in range(4) for j in range(4)])
            if score > max_score:
                max_score = score

        return max_score / (1 << 13)

    def best_move_alphabeta(self, grid: Grid2048, depth: int):
        """
        Returns the best move according to alphabeta algorithm.
        """
        best_score = -math.inf
        best_move = None

        for direction in [EMove.DOWN, EMove.RIGHT, EMove.LEFT, EMove.UP]:
            # Skip direction if not possible to move in this direction.
            if not grid.can_move(direction):
                continue

            grid_clone = grid.clone()
            grid_clone.move_dir(direction)
            # Get alphabeta score for this move.
            score = self.__alphabeta(grid_clone, depth - 1, -math.inf, math.inf, False)

            if score > best_score:
                best_score = score
                best_move = direction

        return best_move

    def __alphabeta(self, grid: Grid2048, depth: int, alpha, beta, maximizing: bool):
        """
        Returns best score for alphabeta algorithm.
        """
        if depth == 0:
            return self.heuristic_score_weighted(grid)

        if maximizing:
            v = -math.inf

            # Move all directions and insert random values
            for direction in [EMove.UP, EMove.LEFT, EMove.RIGHT, EMove.DOWN]:
                if not grid.can_move(direction):
                    continue

                grid_clone = grid.clone()
                grid_clone.move_dir(direction=direction)

                v = max(v, self.__alphabeta(grid_clone, depth - 1, alpha, beta, False))

                alpha = max(v, alpha)
                if alpha >= beta:
                    break

            return v

        else:
            v = math.inf
            empty_cells = grid.get_empty_cells()

            for (x, y) in empty_cells:
                val = 2 if random.uniform(0.0, 1.0) > 0.9 else 4

                grid_clone = grid.clone()
                grid_clone.insert(x, y, val)

                v = min(v, self.__alphabeta(grid_clone, depth - 1, alpha, beta, True))

                beta = min(v, beta)
                if alpha >= beta:
                    break

            return v

    def best_move_expectimax(self, grid: Grid2048, depth: int):
        """
        Returns the best move according to expectimax algorithm.
        """
        best_score = -math.inf
        best_move = None

        for direction in [EMove.DOWN, EMove.RIGHT, EMove.LEFT, EMove.UP]:
            # Skip direction if not possible to move in this direction.
            if not grid.can_move(direction):
                continue

            grid_clone = grid.clone()
            grid_clone.move_dir(direction)
            # Get expectimax score for this move.
            score = self.__expectimax(grid_clone, depth - 1, False)

            if score > best_score:
                best_score = score
                best_move = direction

        return best_move

    def __expectimax(self, grid: Grid2048, depth: int, player: bool):
        """
        Expectimax algorithm
        """
        if depth == 0:
            return self.heuristic_score_weighted(grid)

        if player:
            best_score = -math.inf

            # Move all directions and insert random values
            for direction in [EMove.DOWN, EMove.RIGHT, EMove.LEFT, EMove.UP]:
                # Skip if not possible.
                if not grid.can_move(direction):
                    continue

                grid_clone = grid.clone()
                grid_clone.move_dir(direction)
                score = self.__expectimax(grid_clone, depth - 1, False)

                if score > best_score:
                    best_score = score

            return best_score

        else:
            score = 0
            empty_cells = grid.get_empty_cells()
            size = len(empty_cells)

            for (x, y) in grid.get_empty_cells():
                # Insert a two.
                grid_clone = grid.clone()
                grid_clone.insert(x, y, 2)
                temp_score = 0.9 * self.__expectimax(grid_clone, depth - 1, True)

                if temp_score > 0:
                    score += temp_score

                # Insert a four.
                grid_clone = grid.clone()
                grid_clone.insert(x, y, 4)
                temp_score = 0.1 * self.__expectimax(grid_clone, depth - 1, True)

                if temp_score > 0:
                    score += temp_score

            return score / max(size, 1)
