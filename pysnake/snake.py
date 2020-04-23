# -*- coding: utf-8 -*-
# Created on Sun Feb 16 12:46:25 2020
# @author: arthurd


import numpy as np
import random as rd

# PySnake modules
from pysnake.utils import one_hot_direction
# Snake Game
from pysnake.vision import FullVision
from pysnake.enum import Direction, Item
from pysnake.grid import Cell
# Neural Network
from pysnake.nn.neuralnetwork import NeuralNetwork
# Genetic Algo
from pysnake.gen.individual import Individual
from pysnake.gen.chromosome import Chromosome



class Snake(Individual):
    """
    Define a Snake from Individual abstract class.
    
    
    Attributes
    ----------
    game: pysnake.game.Game
        Game where to initialize the snake.
    seed: int
        Fix random numbers from numpy and random.
    length: int, optional
        The initial length of the snake. 
        Default is 3.
    body: list(pysnake.grid.Cell)
        List of cells composing the snake.
    direction: pysnake.enum.Direction
        Direction of the snake movement.
        This direction is used as input in the neural network.
    tail_direction: 
        Direction of the snake's tail movement.
        This direction is used as input in the neural network.
    bearing: int
        Angle from the north to the snake's direction.
        This attribute is used to rotate the vision making the first ray
        always pointing in front of the snake.
    score: int
        Number of apples the snake ate.
    lifespan: int
        Number of steps the snake survived.
    lifespan_max: int
        Maximal step the snakes can live. 
        When the snake's lifespan reach this number, it dies.
    hunger: int
        Number of steps since the snake ate an apple.
    hunger_max: int
        Maximal step the snake can live without eating an apple.
        When the snake's hunger reach this number, it dies.
    vision_mode: int, optional
        The number of sensors of the snake.
        Default is 8.
    vision_type: str, optional
        Vector representation of the vision.
        Default is "distance". 
    full_vision: pysnake.vision.FullVision
        List of vision oriented from its bearing, equally spaced according to
        vision_mode.
    nn_hidden_layers: list(int)
        Hidden layers dimensions used for the neural network.
    nn_layers_dimension: mist(int)
        Layers dimensions used to create the architecture of the neural network.
    nn_params: dict(numpy.ndarray)
        Neural network parameters for weights, biases and activation output.
        These parameters are used as chromosomes (reshaped as 1D array) 
        in the genetic algorithm.
    """
    
    def __init__(self, game, 
                 length = 3, 
                 vision_max_length = None, 
                 vision_mode = 8, 
                 vision_type = "distance",
                 chromosomes = None,
                 nn_hidden_layers = [20, 12],
                 nn_params = None, 
                 lifespan_max = None,
                 hunger_max = 300, **kwargs):

        
        # Init the snake in a game
        self.game = game
        # Fix the seed, for replay / debug
        self.seed = game.seed
        np.random.seed(self.seed)
        rd.seed(self.seed)
        
        # Body
        self.length = length
        self.body = self._init_body()
        
        # Snake's directions
        self.direction = self._init_direction()
        self.tail_direction = self.get_tail_direction()
        # Change to self.beraing = self._get_bearing() to rotate the vision
        self.bearing = 0
        
        # Stats
        self.score = 0
        self.lifespan = 0
        self.lifespan_max = np.inf if lifespan_max is None else lifespan_max
        self.hunger = 0
        self.hunger_max = np.inf if hunger_max is None else hunger_max
  
        # Vision
        self.vision_mode = vision_mode
        self.vision_type = vision_type
        head = self.body[-1]
        angle = self.bearing
        vision_max_length = None  
        self.full_vision = FullVision(game.grid, head, angle, vision_max_length, vision_mode)
        
        # Neural Network
        self.nn_hidden_layers = nn_hidden_layers
        self.nn_layers_dimension = [self.vision_mode*3 + 4*2] + list(self.nn_hidden_layers) + [4]
        params = self.decode_chromosomes(chromosomes) if chromosomes is not None else nn_params
        self.nn = NeuralNetwork(self.nn_layers_dimension, params=params)
        # Initialize the first activation (the value is used to display the neurons)
        self.next_direction()
        self.nn_params = self.nn.params
                
        # Create chromosomes from the Neural Networks's weights and bias
        chromosomes = self.encode_chromosomes()
        # Create an individual from chromosomes
        super().__init__(chromosomes, **kwargs)
                        
        
    # -------------------------------------------------------------------------
    # Individual Methods
        
    def encode_chromosomes(self):
        """
        Encode chromosomes from NeuralNetwork params weight and bias.

        Returns
        -------
        chromosomes : list(pysnake.gen.chromosome.Chromosome)
            List of chromosome coding the genes from neural network
            weight and bias.
        """
        chromosomes = []
        for (key, param) in self.nn.params.items():
            if key[0] == 'W' or key[0] == 'b':
                chromosome = Chromosome(param.reshape(param.size), id=key, enable_crossover=True)
                chromosomes.append(chromosome)
        return chromosomes
    
    
    def decode_chromosomes(self, chromosomes):
        """
        Transform and reshape chromosomes to Neural Network params.

        Parameters
        ----------
        chromosomes : list(pysnake.gen.chromosome.Chromosome)
            List of chromosome coding the genes from neural network
            weight and bias.
            
        Returns
        -------
        params : dict
            Dict containing weights, biases, activation output of the neural network.
            - W_{i}: weights,
            - b_{i}: biases,
            - A_{i}: activation outputs.
        """
        params = {}
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
        """
        Calculate the fitness / rewards for a snake depending on its score 
        and lifespan.

        Returns
        -------
        None.
        """
        self.fitness = ((self.lifespan) + ((2**self.score) + (self.score**2.1)*500) - 
                        ((.25 * self.lifespan)**1.3 * (self.score**1.2)))
        self.fitness = max(self.fitness, .1)
   
    
    # -------------------------------------------------------------------------
    # Methods
            
    def _get_bearing(self):
        """
        Get the angle from snake's direction to the north.

        Returns
        -------
        bearing : int
            Angle from snake's direction and north.
        """
        bearing = self.direction.value
        return bearing
                    
    
    def _init_body(self):
        """
        Randomly initialize snake's cells, and stack them to its body.

        Returns
        -------
        body : list(pysnake.grid.Cell)
            List of cells composing the snake.
        """
        
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
        """
        Randomly nitialize the snake's direction.

        Returns
        -------
        direction: pysnake.enum.Direction
            Available direction of the snake.
        """
        # Get available cells near its head
        head = self.body[-1]
        head_i, head_j = head.coord
        surrounding_cells = [self.game.grid[head_i - 1, head_j],
                             self.game.grid[head_i + 1, head_j],
                             self.game.grid[head_i, head_j - 1],
                             self.game.grid[head_i, head_j + 1]]
        
        # Select the direction pointing to an empty cell
        possible_cells = []
        for cell in surrounding_cells:
            if cell.item == Item.EMPTY:
                possible_cells.append(cell)
        next_cell = np.random.choice(possible_cells)
        next_i, next_j = next_cell.coord
        
        # Get the direction from the head to this available cell
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
        """
        Tail direction.

        Returns
        -------
        direction: pysnake.enum.Direction
            DESCRIPTION.
        """
        # Difference from two cells
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
        
        
    def get_params(self):
        params = {"length": self.length,
                  "vision_mode": self.vision_mode,
                  "vision_type":self.vision_type,
                  "lifespan_max": self.lifespan_max,
                  "hunger_max": self.hunger_max,
                  "nn_hidden_layers": self.nn_hidden_layers,
                  "nn_params": self.nn_params
                  }
    
        return params
    
    
    
    def kill(self):
        """
        Kill the snake and remove it from the game.

        Returns
        -------
        None.
        """
        for cell in self.body:
            self.game.grid.set_empty(cell.coord)
                 

    def _next_move(self):
        """
        Get the next cell from a direction.

        Returns
        -------
        new_head : pysnake.grid.Cell
            New head cell from a given direction.
        """
        # Get the current head coordinates
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
        """
        Vectorize the snake's vision and its directions.

        Returns
        -------
        X: numpy.ndarray
            One column vector of shape (size_input, 1) used as input vector
            in the neural network.
        """
        # Set the input array for the neural network
        X = np.array([])
        # Binary vision
        if self.vision_type == "binary":
            for vision in self.full_vision:
                X = np.concatenate((X, vision.to_binary()))
        # Distance mode
        else:
            for vision in self.full_vision:
                distances = vision.to_distances()
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
        """
        Get the output from the snake neural network.

        Parameters
        ----------
        X : numpy.ndarray
            One column vector of shape (size_input, 1) used as input vector
            in the neural network.

        Returns
        -------
        Y_hat : numpy.ndarray
            Predicted output of shape (num_class, 1).
        """
        
        Y_hat = self.nn.forward(X)
        return Y_hat
    
    
    def next_direction(self):
        """
        Get the next direction giving the current state.

        Returns
        -------
        next_direction : pysnake.enum.Direction
            The predicted direction to take.
        """
        X = self.compute_input()
        Y = self.compute_output(X)
        # Get the new direction by  the predicted class * 90 (to get the degrees)
        next_direction = Direction(np.argmax(Y) * 90)
        # The snake should follow this new direction
        return next_direction
    
    # @DEPRECATED
    def update_full_vision(self):
        print("Deprectaed. Use snake.update() instead.")
        # Update the bearing
        bearing = self._get_bearing()
        self.bearing = bearing
        head = self.body[-1]
        # Update the vision
        self.full_vision.update(head, bearing)
        
    
    def update(self):
        """
        Update the snake's state when moving.

        Returns
        -------
        None.
        """
        head = self.body[-1]
        self.full_vision.update(head, self.bearing)
        self.tail_direction = self.get_tail_direction()
        
            
    def move(self):
        """
        Move the snake and update the game.

        Returns
        -------
        is_alive: bool
            False if the snake died, True otherwise.
        """
        # Get the current grid
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
            # The snake ate, its hunger decrease
            self.hunger = 0
              
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
            
        # Update its lifespan and hunger
        self.lifespan += 1 
        self.hunger += 1
        
        # Check its lifespan
        if self.lifespan > self.lifespan_max:
            return False
        # Kill it if it didn't get any apples for too long
        elif self.hunger > self.hunger_max:
            return False
        
        # The snake lives !
        return True
        
    
    
    
    