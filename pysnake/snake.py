# -*- coding: utf-8 -*-
# Created on Sun Feb 16 12:46:25 2020
# @author: arthurd



import numpy as np


# PySnake modules
from pysnake.utils import one_hot_direction

# Snake Game
from pysnake.vision import FullVision
from pysnake.enum import Direction, Item
from pysnake.grid import Cell
# Neural Network
from pysnake.nn.mlp import MLP
# Genetic Algo
from pysnake.gen.individual import Individual
from pysnake.gen.chromosome import Chromosome


class Snake(Individual):
    
    def __init__(self, game, 
                 chromosomes = None,
                 nn_hidden_layers = [20, 12],
                 nn_params = None,
                 length = 4, 
                 vision_max_length = None, 
                 vision_mode = 8, 
                 vision_type = "distance", **kwargs):
        
        # The snake can't live without a game !
        self.game = game
        
        self.length = length
        self.vision_mode = vision_mode
        self.vision_type = vision_type
        self.direction = Direction.UP
        self.body = self._create_snake()
        self.bearing = self._get_bearing()
        self.tail_direction = self.get_tail_direction()
        
        # Stats
        self.score = 0
        self.lifespan = 0
  
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
        self.nn_params = self.nn.params
        
        # Create chromosomes from the MLP's weights and bias
        chromosomes = self.encode_chromosomes()
        super().__init__(chromosomes, **kwargs)
                        
        
    # -------------------------------------------------------------------------
    # Re-definition from Individual methods
        
    def encode_chromosomes(self):
        chromosomes = []
        for (key, param) in self.nn.params.items():
            chromosome = Chromosome(param.reshape(param.size), id=key, enable_crossover=True)
            chromosomes.append(chromosome)
        return chromosomes
    
    
    def decode_chromosomes(self, chromosomes):
        params = {}
        assert len(chromosomes) == 2*(len(self.nn_layers_dimension) - 1), (
            "Not enough chromosomes to decode. Please make sure to add the exact number of chromosome to create the MLP.")
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
        
        return params
    
    
    def calculate_fitness(self):
        self.fitness = (self.lifespan) + ((2**self.score) + (self.score**2.1)*500) - ((.25 * self.lifespan)**1.3 * (self.score**1.2))
        self.fitness = max(self.fitness, .1)
        # if self.score < 2 and self.lifespan > 300:
        #     self.fitness = 0
    
    
    # -------------------------------------------------------------------------
    # Unique Methods
        
    
    def _get_bearing(self):
        bearing = self.direction.value
        return bearing
    
    
    def update_full_vision(self):
        # Update the bearing
        bearing = self._get_bearing()
        self.bearing = bearing
        head = self.body[-1]
        # Update the vision
        self.full_vision.update(head, bearing)
                
    
    def _create_snake(self):
        """
        Initialize the snake in the game.

        Parameters
        ----------
        None
        
        Returns
        -------
        body : list(Cell)
            Snake's body, containing all its cells.
        """
                
        body = []
        shape = self.game.shape
        mid_row = shape[0]//2
        mid_col = shape[1]//2
        
        # Body of the snake
        # Last element is its head
        for i in range(self.length-1, -1, -1):
            # The snake is composed by a list of coords
            coord = (mid_row+i, mid_col)
            # Create snake cell
            snake = Cell(coord, Item.SNAKE)
            body.append(snake)
            # Update the game & grid to place the snake
            self.game.grid.set_cell(snake)
        
        return body
   
    
    def get_tail_direction(self):
        tail1 = self.body[0]
        tail2 = self.body[1]
        delta_i = tail1.coord[0] - tail2.coord[0]
        delta_j = tail1.coord[1] - tail2.coord[1]
        if delta_i < 0:
            return Direction.DOWN
        elif delta_i >= 0:
            return Direction.UP
        elif delta_j < 0:
            return Direction.LEFT
        else:
            return Direction.RIGHT
    
    
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
                X = np.concatenate((X, vision.distances))
        
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
    
    
    def update_state(self):
        self.update_full_vision()
        
            
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
            self.update_state()
            
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
            self.update_state()
            
        # Update its lifespan
        self.lifespan += 1 
        if self.lifespan > 1000:
            return False
        if self.lifespan > 100 and self.score <= 2:
            return False
        return True
        
    
    
    
    
    
    