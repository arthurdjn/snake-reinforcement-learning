# -*- coding: utf-8 -*-
# Created on Sun Mar  1 21:20:46 2020
# @author: arthurd


import configparser
from argparse import ArgumentParser

from pysnake.game import GameApplication
from pysnake.snake import load_snake

    


if __name__ == "__main__": 
    
    parser = ArgumentParser()
    parser.add_argument('--config', help="Path to the config.ini file", action='store',
                        type=str, default="pysnake/config.ini")
    parser.add_argument('--mode', help="Mode used, either to play or train snakes", action='store',
                        type=str, default='play')
    parser.add_argument('--loadsnake', help="Load a snake in json format and add it to a game",
                        type=str, default=None)
    
    # Get the arguments    
    args = parser.parse_args()
    config_file = args.config
    mode = args.mode.lower()
    loadsnake = args.loadsnake
    
    # Load the game
    config = configparser.ConfigParser()
    config.read(config_file)
    
    
    # Keys
    print("\nDirections")
    print("\tUP \t\t\t: Up arrow")
    print("\tLEFT \t\t\t: Left arrow")
    print("\tDOWN \t\t\t: Down arrow")
    print("\tRIGHT \t\t\t: Right arrow")
    print("Optional")
    print("\tShow snake's vision \t: V")
    print("\tShow the grid      \t: G")
    print("\tIncrease the fps   \t: +")
    print("\tDecrease the fps   \t: -")
        
    snake_game = GameApplication(config)
    
    if type(loadsnake) is str:
        snake = load_snake('../saves/snake.json')
        snake_game.play(snake)
    elif mode == 'play':
        snake_game.play()
    else:       
        snake_game.train()
        
    
    