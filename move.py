from enum import Enum


class EMove(Enum):
    LEFT = 1,
    RIGHT = 2,
    UP = 3,
    DOWN = 4,
    INVALID = 5,
    CONTINUE = 6,


class LinkedMove:
    """
    Linked list kind of data structure.
    This is for backtracking the moves made.
    """

    def __init__(self, my_move, pre_move):
        self.my_move = my_move
        self.pre_move = pre_move