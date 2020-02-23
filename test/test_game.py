# -*- coding: utf-8 -*-
# Created on Wed Feb 19 20:29:15 2020
# @author: arthurd

from pysnake.enum import Item
from pysnake import Game, Cell


def test_game():
    
    # ----------
    # Parameters
    # ----------
    
    shape = (10, 10)
    
    game = Game(shape)
    print("\t1/ Game shape {}".format(game.shape))
    print("\t2/ Game grid  {}".format(game.grid.shape))
    print(game.grid)



if __name__ == "__main__":
    
    # Testing Game
    print("Testing Game...")
    test_game()
    print("Game tested.")
    
    