import math
import random

from Move import EMove, LinkedMove
from grid_2048 import Grid2048


class Engine2048:

    def __init__(self):
        self.bestMove = EMove.LEFT
        self.linked_move = None
        self.actualScore = 0
        self.G = None

        w1 = [[1 << 15, 1 << 14, 1 << 13, 1 < 12],
              [1 << 8, 1 << 9, 1 << 10, 1 << 11],
              [1 << 7, 1 << 6, 1 << 5, 1 << 4],
              [1, 1 << 1, 1 << 2, 1 << 3]]

        w2 = [[1 << 12, 1 << 13, 1 << 14, 1 < 15],
              [1 << 11, 1 << 10, 1 << 9, 1 << 8],
              [1 << 4, 1 << 5, 1 << 6, 1 << 7],
              [1 << 3, 1 << 2, 1 << 1, 1]]

        w3 = [[1 << 3, 1 << 2, 1 << 1, 1],
              [1 << 4, 1 << 5, 1 << 6, 1 << 7],
              [1 << 11, 1 << 10, 1 << 9, 1 << 8],
              [1 << 12, 1 << 13, 1 << 14, 1 << 15]]

        w4 = [[1, 1 << 1, 1 << 2, 1 < 3],
              [1 << 7, 1 << 6, 1 << 5, 1 << 4],
              [1 << 8, 1 << 9, 1 << 10, 1 << 11],
              [1 << 15, 1 << 14, 1 << 13, 1 << 12]]

        w5 = [[1 << 15, 1 << 8, 1 << 7, 1],
              [1 << 14, 1 << 9, 1 << 6, 1 << 1],
              [1 << 13, 1 << 10, 1 << 5, 1 << 2],
              [1 << 12, 1 << 11, 1 << 4, 1 << 3]]

        w6 = [[1 << 12, 1 << 11, 1 << 4, 1 < 3],
              [1 << 13, 1 << 10, 1 << 5, 1 << 2],
              [1 << 14, 1 << 9, 1 << 6, 1 << 1],
              [1 << 15, 1 << 8, 1 << 7, 1]]

        w7 = [[1 << 3, 1 << 4, 1 << 11, 1 < 12],
              [1 << 2, 1 << 5, 1 << 10, 1 << 13],
              [1 << 1, 1 << 6, 1 << 9, 1 << 14],
              [1, 1 << 7, 1 << 8, 1 << 15]]

        w8 = [[1, 1 << 7, 1 << 8, 1 < 15],
              [1 << 1, 1 << 6, 1 << 9, 1 << 14],
              [1 << 2, 1 << 5, 1 << 10, 1 << 13],
              [1 << 3, 1 << 4, 1 << 11, 1 << 12]]

        self.weights = [w1, w2, w3, w4, w5, w6, w7, w8]

    def heuristic_score_weighted(self, G: Grid2048):

        max_score = -math.inf

        for weights in self.weights:

            score = 0
            for i in range(4):
                for j in range(4):
                    score += weights[i][j] * G.grid[i][j]

                    if score > max_score:
                        max_score = score

        return max_score / (1 << 13)

    def alphabeta(self, G: Grid2048, depth: int, alpha, beta, maximizing: bool):
        if depth == 0:
            return self.heuristic_score_weighted(G)

        if maximizing:
            v = -math.inf

            # Move all directions and insert random values
            for direction in [EMove.UP, EMove.LEFT, EMove.RIGHT, EMove.DOWN]:
                if not G.can_move(direction):
                    continue

                GG = G.clone()
                GG.move_dir(direction=direction)

                v = max(v, self.alphabeta(GG, depth - 1, alpha, beta, False))

                if v > alpha:
                    self.bestMove = direction

                alpha = max(v, alpha)

                if beta <= alpha:
                    break

            return v

        else:
            v = math.inf

            empty_cells = G.get_empty_cells()
            opponent_moves = [2, 4]

            for ec in empty_cells:
                x, y = ec
                for om in opponent_moves:
                    GG = G.clone()
                    GG.insert(x, y, om)

                    v = min(v, self.alphabeta(GG, depth - 1, alpha, beta, True))

                    beta = min(v, beta)

                    if beta <= alpha:
                        break

            return v

    def alphabeta_prob(self, G: Grid2048, move: LinkedMove, depth: int, alpha, beta, maximizing: bool):
        if depth == 0:
            return self.heuristic_score_weighted(G)

        if maximizing:
            v = -math.inf

            # Move all directions and insert random values
            for direction in [EMove.UP, EMove.LEFT, EMove.RIGHT, EMove.DOWN]:
                if not G.can_move(direction):
                    continue

                GG = G.clone()
                GG.move_dir(direction=direction)

                lmove = LinkedMove(direction, move)

                v = max(v, self.alphabeta_prob(GG, lmove, depth - 1, alpha, beta, False))

                if v > alpha:
                    self.bestMove = direction
                    self.linked_move = lmove

                alpha = max(v, alpha)

                if beta <= alpha:
                    break

            return v

        else:
            v = math.inf
            empty_cells = G.get_empty_cells()

            for ec in empty_cells:
                x, y = ec

                val = 2
                if random.uniform(0.0, 1.0) > 0.8:
                    val = 4

                GG = G.clone()
                GG.insert(x, y, val)

                v = min(v, self.alphabeta_prob(GG, move, depth - 1, alpha, beta, True))

                beta = min(v, beta)

                if beta <= alpha:
                    break

            return v

