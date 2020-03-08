# -*- coding: utf-8 -*-
# Created on Fri Mar  6 12:46:41 2020
# @author: arthurd


# Read the config file
import configparser
# PySnake module
from pysnake.game import GameApplication
from pysnake.io import load_snake


if __name__ == "__main__":
    
    # Load the game
    config = configparser.ConfigParser()
    config_file = "config.ini"
    config.read(config_file)
    snake_game = GameApplication(config)
    
    # Load the initial snake (Optional)
    snake_file = "snake.json"
    snake = load_snake(snake_file)
    
    # Play from an existing snake
    snake_game.play(snake)
    
    
    
    