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

        gridLeft.move_left(put_rand=True)
        gridRight.move_right(put_rand=True)
        gridUp.move_up(put_rand=True)
        gridDown.move_down(put_rand=True)

        return [gridLeft, gridRight,gridUp,gridDown]


    def heuristic_score(self, G: Grid2048):
        return G.largest_in_upper_left_corner()


    def alphabeta(self, G: Grid2048, depth: int, alpha, beta, maximizing: bool):
        if depth == 0:
            return self.heuristic_score(G)

        if maximizing:
            v = -math.inf

            # Move all directions and insert random values
            grids = self.move_board_all_directions(G)

            for grid in grids:
                v = max(v, self.alphabeta(grid, depth-1, alpha, beta, False))

                if v > alpha:
                    self.bestMove = grid.moved

                alpha = max(v, alpha)

                if beta <= alpha:
                    break

            return v

        else:
            v = math.inf
            grids = [G]

            for grid in grids:
                empty_cells = grid.get_empty_cells()
                opponent_moves = [2]

                for ec in empty_cells:
                    x, y = ec
                    for om in opponent_moves:
                        GG = grid.clone()
                        GG.insert(x, y, om)

                        v = min(v, self.alphabeta(GG, depth-1, alpha, beta, True))

                        beta = min(v, beta)

                        if beta <= alpha:
                            break


            return v
