# -*- coding: utf-8 -*-
# Created on Fri Mar  6 00:00:43 2020
# @author: arthurd


# Useful packages
import os
import json
import numpy as np
# PySnake modules
from pysnake.snake import Snake
import pysnake.game
from pysnake.gen.population import Population



def open_files(dir_path, ext="json"):
    """
    Get the path of all files in a directory

    Parameters
    ----------
    dir_path : string
        Name or path to the directory where the files you want to
        open are saved..
    ext : string, optional
        The files extension you want to open. The default is "json".

    Returns
    -------
    list
        A list of the path of all files saved in the directory, with the extension
        json by default.
   

    Example
    -------
        >>> dir_name = "saves/generation_0"
        >>> files = open_files(dir_name, ext="geojson")
        >>> files
            ['saves/generation_0/snake_1.json',
             'saves/generation_0/snake_2.json',
             'saves/generation_0/snake_3.json',
             #...
             'saves/generation_0/snake_1499.json']
    """
    try :
        ls = os.listdir(dir_path)
    except FileNotFoundError :
        raise FileNotFoundError("directory not found")
    files_list = []
    for f in ls :
        if f.endswith(ext):
            filename = os.path.join(dir_path, f)
            files_list.append(filename)
    return files_list


def save_snake(snake, filename, dirpath = '.'):
    """
    Save a Snake in json format.

    Parameters
    ----------
    snake : pysnake.snake.Snake
        Snake to save.
    filename : str
        Name of the file.
    dirpath : str, optional
        Path to the directory to save the file.
        The default is '.'.

    Returns
    -------
    None.
    """
    data = {'id': snake.id,
            'game_shape': snake.game.shape,
            'seed': snake.seed,
            'score': snake.score,
            'lifespan': snake.lifespan,
            'lifespan_max': snake.lifespan_max,
            'hunger_max': snake.hunger_max,
            'length': snake.length,
            'vision_mode': snake.vision_mode,
            'vision_type': snake.vision_type,
            'nn_hidden_layers': snake.nn_hidden_layers,
            'body': [],
            'params': {}}
    
    for (key, param) in snake.nn.params.items():
        data['params'][key] =  param.tolist()
    
    for cell in snake.body:
        data['body'].append({'coord': cell.coord,
                             'item': cell.item.name,
                             'value': cell.value})
            
    # Save it !
    if filename.split('.')[-1] != 'json':
        filename += '.json'
        
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)
        
    with open(dirpath + os.sep + filename, 'w') as f:
        json.dump(data, f)   

        
def load_snake(filename, game=None, keepseed=True):
    """
    Load a Snake from a json file.

    Parameters
    ----------
    filename : str
        Name of the file to open.
    game : pysnake.game.Game, optional
        Game in which to add the Snake.
        The default is None.
    keepseed : bool, optional
        Load the Snake with seed, for Game and Snake. 
        The default is True.

    Returns
    -------
    snake : pysnake.snake.Snake
        Loaded Snake.
    """
    # Open the file
    with open(filename) as f:
        data = json.load(f)
    
    if game is None:
        shape = data['game_shape']
        seed = None
        if keepseed:
            seed = data['seed']
        game = pysnake.game.Game(shape, seed = seed)
    
    params = {}
    for (key, param) in data['params'].items():
        params[key] = np.array(param)
        
    snake = Snake(game, 
                  nn_params=params, 
                  vision_type=data['vision_type'],
                  vision_mode=data['vision_mode'], 
                  length=data['length'], 
                  id=data['id'])
    # Snake is init
    # previous_body = snake.body
    # for cell in previous_body:
    #     snake.game.grid.set_empty(cell.coord)
    # snake.body = [Cell(cell['coord'], Item.SNAKE) for cell in data['body']]
    # snake.game.grid.set_cell(*snake.body)

    return snake


def load_params(filename):
    """
    Load only Neural Network params from a snake json file.

    Parameters
    ----------
    filename : str
        Name of the file to load.

    Returns
    -------
    params : dict
        Neural Network params for weights, biases and activation outputs.
        - W_{i}: weights,
        - b_{i}: biases,
        - A_{i}: activation outputs.
    """
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


def load_population(dirpath, game=None):
    """
    Load a population made of snake json files in a directory.

    Parameters
    ----------
    dirpath : str
        Path to the directory in which all individuals are saved in a json format.
    game : pysnake.game.Game, optional
        Game in which to add the population. 
        The default is None.

    Returns
    -------
    pysnake.gen.population.Population
        Loaded population.
    """
    individuals = []
    files = open_files(dirpath, ext='json')
    for file in files:
        snake = load_snake(file)
        individuals.append(snake)
    return Population(individuals)




