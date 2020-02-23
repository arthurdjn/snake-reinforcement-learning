# -*- coding: utf-8 -*-
# Created on Wed Feb 19 18:46:47 2020
# @author: arthurd

import random as rd
# Fix the seed to always pick up random values the same way
rd.seed(42)


# Import PySnake modules
from pysnake.enum import Item
from pysnake.grid import Cell

from pysnake.utils import cell_to_coord, cell_to_name, cell_to_item


def test_cell_to():
    
    cells = []
    for i in range(21):
        coord = (i, 2*i)
        item = rd.choices([Item.EMPTY, Item.APPLE, Item.SNAKE])[0]
        cell = Cell(coord, item)
        cells.append(cell)
        
    cells_coord = cell_to_coord(*cells)
    cells_name = cell_to_name(*cells)
    cells_item = cell_to_item(*cells)
    print(cells_coord)
    print(cells_name)
    print(cells_item)





if __name__ == "__main__":
    
    # cell_to
    print("Testing cell_to...()...")
    test_cell_to()
    print("Tested cell_to...().")
    
    
    
    