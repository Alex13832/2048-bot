import math
import random

from move import EMove, LinkedMove
from grid_2048 import Grid2048


class Engine2048:

    def __init__(self):
        self.bestMove = EMove.LEFT
        self.linked_move = None

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
        """
        Computes the heuristic score for the input grid.
        :param G: input grid.
        :return: score.
        """
        max_score = -math.inf

        for weights in self.weights:
            score = sum([weights[i][j] * G.grid[i][j] for i in range(4) for j in range(4)])
            max_score = max(max_score, score)

        # Divide the score by 2^13
        return max_score / (1 << 13)

    def alphabeta_prob(self, game: Grid2048, move: LinkedMove, depth: int, alpha, beta, maximizing: bool):
        """
        Mini-max algorithm with alpha-beta pruning.
        Maximize-step: Find best move of left, right, up and down, update if local score is better than known best.
        Minimize-step: Insert random two or four. P(2) = 0.8, P(4) = 1.0 - P(2) = 0.2.
        :param game: Grid.
        :param move: tracked moves.
        :param depth: search depth.
        :param alpha:
        :param beta:
        :param maximizing:
        :return: best score.
        """
        if depth == 0:
            return self.heuristic_score_weighted(game)

        if maximizing:
            v = -math.inf

            # Move all directions and insert random values
            for direction in [EMove.UP, EMove.LEFT, EMove.RIGHT, EMove.DOWN]:
                if not game.can_move(direction):
                    continue

                game_cloned = game.clone()
                game_cloned.move_dir(direction=direction)

                lmove = LinkedMove(direction, move)
                lmove.pre_move = move

                v = max(v, self.alphabeta_prob(game_cloned, lmove, depth - 1, alpha, beta, False))

                if v > alpha:
                    self.bestMove = direction
                    self.linked_move = lmove

                alpha = max(v, alpha)

                if beta <= alpha:
                    break

            return v

        else:
            v = math.inf
            empty_cells = game.get_empty_cells()

            for ec in empty_cells:
                x, y = ec

                # Insert random two or four, two is more probable.
                val = 2
                if random.uniform(0.0, 1.0) > 0.8:
                    val = 4

                game_cloned = game.clone()
                game_cloned.insert(x, y, val)

                v = min(v, self.alphabeta_prob(game_cloned, move, depth - 1, alpha, beta, True))
                beta = min(v, beta)

                if beta <= alpha:
                    break

            return v
