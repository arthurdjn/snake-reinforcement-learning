# -*- coding: utf-8 -*-
# Created on Sun Mar  1 21:20:46 2020
# @author: arthurd


import configparser

from pysnake.game import GameApplication
from pysnake.snake import load_snake

    
if __name__ == "__main__":
    
    config = configparser.ConfigParser()
    config.read("config.ini")

    # Run
    # ---
    snake_game = GameApplication(config)
    
    # Play
    # ----
    snake_game.play()
    
    # Load a snake
    # snake = load_snake('../saves/snake.json')
    # snake_game.play(snake)
    
    # Train
    # -----
    # snake_game.train()

    
