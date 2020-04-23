# -*- coding: utf-8 -*-
# Created on Sun Mar  1 21:20:46 2020
# @author: arthurd


import configparser
from argparse import ArgumentParser

from pysnake.game import GameApplication
from pysnake.snake import Snake
from pysnake.io import load_params, load_population, load_snake
    


if __name__ == "__main__": 
    
    parser = ArgumentParser()
    parser.add_argument('--config', help="Path to the config.ini file", action='store',
                        type=str, default="pysnake/config.ini")
    parser.add_argument('--mode', help="Mode used, either to play or train snakes", action='store',
                        type=str, default='play')
    parser.add_argument('--snake', help="Load a snake in json format and add it to a new game.",
                        type=str, default=None)
    parser.add_argument('--replay', help="Replay a snake game.",
                        type=str, default=None)
    parser.add_argument('--population', help="Train from an existing population.",
                        type=str, default=None)
    # Get the arguments    
    args = parser.parse_args()
    config_file = args.config
    mode = args.mode.lower()
    snake_file = args.snake
    snake_replay_file = args.replay
    population_file = args.population
    
    # Load the game
    config = configparser.ConfigParser()
    config.read(config_file)
    
    
    # Keys
    print("\nDirections")
    print("\tUP                     : Up    arrow")
    print("\tLEFT                   : Left  arrow")
    print("\tDOWN                   : Down  arrow")
    print("\tRIGHT                  : Right arrow")
    print("Optional")
    print("\tRestart                : R")
    print("\tShow snake's vision    : V")
    print("\tShow the grid          : G")
    print("\tIncrease the fps       : +")
    print("\tDecrease the fps       : -")
        
    snake_game = GameApplication(config)
    
    if snake_file is not None:
        snake = load_snake(snake_file, keepseed=False)
        snake_game.play(snake)
    elif snake_replay_file is not None:
        snake = load_snake(snake_replay_file, keepseed=True)
        snake_game.play(snake)
    elif population_file is not None:
        population = load_population(population_file)
        snake_game.train(population_file)
    elif mode == 'play':
        snake_game.play()
    else:       
        snake_game.train()
        
    
    