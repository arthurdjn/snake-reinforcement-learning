# -*- coding: utf-8 -*-
# Created on Wed Feb 19 11:30:19 2020
# @author: arthurd

from enum import Enum


class Direction(Enum):
    # In degrees
    # Origin is toward the North
    UP    = 0
    LEFT  = 90
    DOWN  = 180
    RIGHT = 270


class Item(Enum):
    WALL  = 0
    SNAKE = 1
    APPLE = 2
    
    # Empty MUST have the last index
    # For one-hot encoded vectors simplification
    EMPTY = 3




