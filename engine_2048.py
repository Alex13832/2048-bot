from grid_2048 import Grid2048
from enum import Enum
import math
import numpy as np
from Move import EMove

class Engine2048:

    def __init__(self):
        self.bestMove = EMove.LEFT
        self.actualScore = 0


    def move_board_all_directions(self, Grid: Grid2048):
        """
        Moves the Grid in all directions
        """
        gridLeft = Grid.clone()
        gridRight = Grid.clone()
        gridUp = Grid.clone()
        gridDown = Grid.clone()

        gridLeft.move_left(put_rand=False)
        gridRight.move_right(put_rand=False)
        gridUp.move_up(put_rand=False)
        gridDown.move_down(put_rand=False)

        return [gridLeft, gridUp, gridRight, gridDown]


    def heuristic_score(self, G: Grid2048):
        ls = max(1, G.compute_score())
        cs = G.clustering_score()

        score = ls + math.log(ls) * G.number_of_empty() - cs + 10*G.largest_in_upper_left_corner()
        return max(score, min(ls, 1))

    def heuristic_score_weighted(self, G: Grid2048):

        weights = [
            [4**6, 4**5, 4**4, 4**3],
            [4**5, 4**4, 4**3, 4**2],
            [4**4, 4**3, 4**2, 4**1],
            [4**3, 4**2, 4**1, 1]
        ]

        score = 0
        for i in range(4):
            for j in range(4):
                score += weights[j][i] * G.grid[j][i]

        return score


    def alphabeta(self, G: Grid2048, depth: int, alpha, beta, maximizing: bool):
        if depth == 0:
            #return self.heuristic_score(G)
            return self.heuristic_score_weighted(G)

        if maximizing:
            v = -math.inf

            # Move all directions and insert random values
            for direction in [EMove.LEFT, EMove.UP, EMove.DOWN, EMove.RIGHT]:
                if not G.can_move(direction):
                    continue

                GG = G.clone()
                GG.move_dir(dir=direction)

                v = max(v, self.alphabeta(GG, depth-1, alpha, beta, False))

                if v > alpha:
                    self.bestMove = direction

                alpha = max(v, alpha)

                if beta <= alpha:
                    break

            return v

        else:
            v = math.inf

            empty_cells = G.get_empty_cells()
            opponent_moves = [2]

            for ec in empty_cells:
                x, y = ec
                for om in opponent_moves:
                    GG = G.clone()
                    GG.insert(x, y, om)

                    v = min(v, self.alphabeta(GG, depth-1, alpha, beta, True))

                    beta = min(v, beta)

                    if beta <= alpha:
                        break


            return v
