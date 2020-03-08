# -*- coding: utf-8 -*-
# Created on Wed Feb 19 11:30:19 2020
# @author: arthurd

from enum import Enum


class Direction(Enum):
    """
    Enumerate all four directions.
    """
    # In degrees
    # Origin is toward the North
    UP    = 0
    LEFT  = 90
    DOWN  = 180
    RIGHT = 270


class Item(Enum):
    """
    Enumerate all items in the game.
    """
    # For one-hot encoded vectors simplification
    EMPTY = -1
    # Non-empty items values should start at 0
    WALL  = 0
    SNAKE = 1
    APPLE = 2
    





