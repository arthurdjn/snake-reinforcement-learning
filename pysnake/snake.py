# -*- coding: utf-8 -*-
# Created on Sun Feb 16 12:46:25 2020
# @author: arthurd



import numpy as np
import random as rd
import json

# PySnake modules
from pysnake.utils import one_hot_direction
# Snake Game
from pysnake.vision import FullVision
from pysnake.enum import Direction, Item
from pysnake.grid import Cell
import pysnake.game as gm
# Neural Network
from pysnake.nn.mlp import MLP
# Genetic Algo
from pysnake.gen.individual import Individual
from pysnake.gen.chromosome import Chromosome



class Snake(Individual):
    
    def __init__(self, game, 
                 length = 3, 
                 vision_max_length = None, 
                 vision_mode = 8, 
                 vision_type = "distance",
                 chromosomes = None,
                 nn_hidden_layers = [20, 12],
                 nn_params = None, 
                 max_lifespan = None, **kwargs):
        
        # The snake can't live without a game !
        self.game = game
        
        self.length = length
        self.vision_mode = vision_mode
        self.vision_type = vision_type
        self.body = self._create_snake()
        
        # Bearing is optional.
        # If Bearing is set to self._get_bearing(), it will orientate the vision
        # in front of it
        # In that case, make sure to update update_full_vision()
        # Initialize a random direction
        self.direction = self._init_direction()
        self.bearing = 0
        self.tail_direction = self.get_tail_direction()
        
        # Stats
        self.score = 0
        self.lifespan = 0
        self.max_lifespan = np.inf if max_lifespan is None else max_lifespan
  
        # Vision
        head = self.body[-1]
        angle = self.bearing
        vision_max_length = None  
        self.full_vision = FullVision(game.grid, head, angle, vision_max_length, vision_mode)
        
        # Neural Network
        self.nn_hidden_layers = nn_hidden_layers
        self.nn_layers_dimension = [self.vision_mode*3 + 4*2] + list(self.nn_hidden_layers) + [4]
        params = self.decode_chromosomes(chromosomes) if chromosomes is not None else nn_params
        self.nn = MLP(self.nn_layers_dimension, params=params)
        self.next_direction()
        self.nn_params = self.nn.params
        
        # Create chromosomes from the MLP's weights and bias
        chromosomes = self.encode_chromosomes()
        super().__init__(chromosomes, **kwargs)
                        
        
    # -------------------------------------------------------------------------
    # Individual Methods
        
    def encode_chromosomes(self):
        chromosomes = []
        for (key, param) in self.nn.params.items():
            chromosome = Chromosome(param.reshape(param.size), id=key, enable_crossover=True)
            chromosomes.append(chromosome)
        return chromosomes
    
    
    def decode_chromosomes(self, chromosomes):
        params = {}
        # assert len(chromosomes) == 2*(len(self.nn_layers_dimension) - 1), (
        #     "Not enough chromosomes to decode. Please make sure to add the exact number of chromosome to create the MLP.")
        for chromosome in chromosomes:
            params[chromosome.id] = chromosome.genes
            
        for (key, param) in params.items():
            if key[0] == 'W':
                idx = int(key[-1])
                shape = (self.nn_layers_dimension[idx-1], self.nn_layers_dimension[idx])
                params[key] = param.reshape(shape)
            elif key[0] == 'b':
                shape = (param.size, 1)
                params[key] = param.reshape(shape)
            elif key[0] == 'A':
                shape = (param.size, 1)
                params[key] = param.reshape(shape)     
        
        return params
    
    
    def calculate_fitness(self):
        self.fitness = (self.lifespan) + ((2**self.score) + (self.score**2.1)*500) - ((.25 * self.lifespan)**1.3 * (self.score**1.2))
        self.fitness = max(self.fitness, .1)
   
    
    # -------------------------------------------------------------------------
    # Methods
            
    def _get_bearing(self):
        bearing = self.direction.value
        return bearing
    
    
    def update_full_vision(self):
        # Update the bearing
        # bearing = self._get_bearing()
        # self.bearing = bearing
        head = self.body[-1]
        # Update the vision
        self.full_vision.update(head, self.bearing)
                
    
    def _create_snake(self):
                
        body = []
        shape = self.game.shape
       
        # Tail position
        tail_i = rd.randint(1 + self.length, shape[0] - 2 - self.length)
        tail_j = rd.randint(1 + self.length, shape[1] - 2 - self.length)

        coord = (tail_i, tail_j)
        body_set = {coord}
        snake_cell = Cell(coord, Item.SNAKE)
        body.append(snake_cell)
        self.game.grid.set_cell(snake_cell)
        
        # Body of the snake
        # Last element is its head
        for _ in range(self.length - 1):
            i, j = coord
            possible_coord = list({(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)} - body_set)
            idx = np.random.choice(np.arange(len(possible_coord)))
            coord = possible_coord[idx]
            snake_cell = Cell(coord, Item.SNAKE)
            body.append(snake_cell)
            body_set = body_set.union({coord})
            self.game.grid.set_cell(snake_cell)     
        
        return body
    
    
    def _init_direction(self):
        
        head = self.body[-1]
        head_i, head_j = head.coord
        surrounding_cells = [self.game.grid[head_i - 1, head_j],
                             self.game.grid[head_i + 1, head_j],
                             self.game.grid[head_i, head_j - 1],
                             self.game.grid[head_i, head_j + 1]]
        possible_cells = []
        for cell in surrounding_cells:
            if cell.item == Item.EMPTY:
                possible_cells.append(cell)
        next_cell = np.random.choice(possible_cells)
        next_i, next_j = next_cell.coord

        delta_i = head_i - next_i
        delta_j = head_j - next_j
        if delta_i < 0 and delta_j == 0:
            return Direction.DOWN
        elif delta_i > 0 and delta_j == 0:
            return Direction.UP
        elif delta_j < 0 and delta_i == 0:
            return Direction.RIGHT
        else:
            return Direction.LEFT
        
    
    def get_tail_direction(self):
        tail1 = self.body[0]
        tail2 = self.body[1]
        delta_i = tail1.coord[0] - tail2.coord[0]
        delta_j = tail1.coord[1] - tail2.coord[1]
        if delta_i < 0 and delta_j == 0:
            return Direction.DOWN
        elif delta_i > 0 and delta_j == 0:
            return Direction.UP
        elif delta_j < 0 and delta_i == 0:
            return Direction.RIGHT
        else:
            return Direction.LEFT
    
    
    def kill(self):
        for cell in self.body:
            self.game.grid.set_empty(cell.coord)
                 

    def _next_move(self):
        head = self.body[-1] # Last element
        head_coord = head.coord
        
        # Switch / Case for all directions
        if self.direction is Direction.UP:
            new_head_coord = (head_coord[0] - 1, head_coord[1])
        elif self.direction is Direction.LEFT:
            new_head_coord = (head_coord[0], head_coord[1] - 1)
        elif self.direction is Direction.DOWN:
            new_head_coord = (head_coord[0] + 1, head_coord[1])     
        elif self.direction is Direction.RIGHT:
            new_head_coord = (head_coord[0], head_coord[1] + 1)       
        
        # Create the new head
        new_head = Cell(new_head_coord, Item.SNAKE)
        
        return new_head
       
    
    def compute_input(self):
        vision_type = self.vision_type
        # Set the input array for the neural network
        X = np.array([])
        # Binary vision
        if vision_type == "binary":
            for vision in self.full_vision:
                X = np.concatenate((X, vision.to_one_hot()))
        # Distance mode
        else:
            for vision in self.full_vision:
                distances = vision.to_distances()
                # diag = np.linalg.norm((self.game.shape[0] - 2, self.game.shape[1] - 2))
                normalized_distances = np.divide(1, distances, 
                                                 out=np.zeros_like(distances), 
                                                 where=distances!=0)
                X = np.concatenate((X, normalized_distances))
        
        # Add the one hot encoded direction vectors
        one_hot_tail = one_hot_direction(self.tail_direction)
        X = np.concatenate((X, one_hot_tail))
        # Idem for its direction
        one_hot = one_hot_direction(self.direction)
        X = np.concatenate((X, one_hot))
                
        return X[:, np.newaxis]
    
    
    def compute_output(self, X):
        Y_hat = self.nn.forward(X)
        return Y_hat
    
    
    def next_direction(self):
        X = self.compute_input()
        Y = self.compute_output(X)
        # Get the new direction by  the predicted class * 90 (to get the degrees)
        next_direction = Direction(np.argmax(Y) * 90)
        return next_direction
    
    
    def update(self):
        self.update_full_vision()
        self.tail_direction = self.get_tail_direction()
        
            
    def move(self):
        """
        Move the snake and update the game.

        Returns
        -------
        bool
            False if the snake died.
        """
        
        grid = self.game.grid
        new_head = self._next_move()
        # First, test if the move is valid
        if grid.is_outside(new_head):
            # The snake died
            return False
        elif grid.is_wall(new_head):
            # The snake died
            return False
        
        # Then test if it eat itself
        elif grid.is_snake(new_head):
            # The snake died
            return False
        
        # Test if it grows
        elif grid.is_apple(new_head):
            # Update the body
            self.body.append(new_head)
   
            # Update the game / grid
            grid.set_cell(new_head)   
            self.game.add_apple()
            
            # Update the vision & state
            self.update()
            
            # Update the stats
            self.score += 1
              
        # Move the snake
        else:
            # Update the body
            self.body.append(new_head)
            previous_tail = self.body.pop(0)
            
            # Update the game
            grid.set_cell(new_head)
            grid.set_empty(previous_tail.coord)
            
            # Update the vision & state
            self.update()
            
        # Update its lifespan
        self.lifespan += 1 
        if self.lifespan > self.max_lifespan:
            return False
        if self.lifespan > 100 and self.score < 1:
            return False
        
        return True
        
    
    
def save_snake(snake, filename):
    data = {'id': snake.id,
            'game_shape': snake.game.shape,
            'score': snake.score,
            'lifespan': snake.lifespan,
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
    with open(filename, 'w') as f:
        json.dump(data, f)   

    
    
def load_snake(filename, game=None):
    # Open the file
    with open(filename) as f:
        data = json.load(f)
    
    if game is None:
        shape = data['game_shape']
        game = gm.Game(shape)
    
    params = {}
    for (key, param) in data['params'].items():
        params[key] = np.array(param)
        
    snake = Snake(game, 
                  nn_params=params, 
                  vision_type=data['vision_type'],
                  vision_mode=data['vision_mode'], 
                  length=data['length'], 
                  id=data['id'])
    previous_body = snake.body
    for cell in previous_body:
        snake.game.grid.set_empty(cell.coord)
    snake.body = [Cell(cell['coord'], Item.SNAKE) for cell in data['body']]
    snake.game.grid.set_cell(*snake.body)

    return snake

    
    
    