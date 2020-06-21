from enum import Enum


class EMove(Enum):
    LEFT = 1,
    RIGHT = 2,
    UP = 3,
    DOWN = 4,


class LinkedMove:
    """
    Linked list kind of data structure.
    """

    def __init__(self, my_move, pre_move):
        self.my_move = my_move
        self.pre_move = pre_move
