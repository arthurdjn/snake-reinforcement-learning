# -*- coding: utf-8 -*-
# Created on Sun Feb 16 22:18:39 2020
# @author: arthurd

"""
Usefull functions for debugging and displaying better grid.
"""


import numpy as np
import json


# Extract coordinates from cells
def cell2coord(*cells):
    return [cell.coord for cell in cells]

def cell2name(*cells):
    return [cell.name for cell in cells]

def cell2item(*cells):
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




def load_params(filename):
    # Open the file
    with open(filename) as f:
        data = json.load(f)
    
    params = {'length': data['length'],
              'id': data['id'],
              'vision_mode': data['vision_mode'],
              'vision_type': data['vision_type'],
              'nn_params': {}
              }
    
    for (key, param) in data['params'].items():
        params['nn_params'][key] = np.array(param)
    
    return params





