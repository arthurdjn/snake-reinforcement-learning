# -*- coding: utf-8 -*-
# Created on Sun Feb 16 22:18:39 2020
# @author: arthurd

"""
Usefull functions for debugging and displaying better grid.
"""


import numpy as np


# Extract coordinates from cells
def cell_to_coord(*cells):
    return [cell.coord for cell in cells]

def cell_to_name(*cells):
    return [cell.name for cell in cells]

def cell_to_item(*cells):
    return [cell.item for cell in cells]


# One hot encoded vectors
def one_hot_vector(y, num_class):
    y_tilde = np.zeros(num_class)
    y_tilde[y] = 1
    return y_tilde

def one_hot_direction(direction):
    y_tilde = np.zeros(4)
    y_tilde[direction.value // 90] = 1
    return y_tilde
