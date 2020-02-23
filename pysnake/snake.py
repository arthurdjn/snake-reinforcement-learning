# -*- coding: utf-8 -*-
# Created on Sun Feb 16 12:46:25 2020
# @author: arthurd



import numpy as np


# PySnake modules
from pysnake.utils import one_hot_direction

from pysnake.vision import FullVision
from pysnake.enum import Direction, Item
from pysnake.grid import Cell



class Snake:
    
    def __init__(self, game, 
                 length = 3, 
                 vision_max_length = None, 
                 vision_mode = 16, 
                 vision_type = "distance"):
        
        # The snake can't live without a game !
        self.game = game
        
        # Attributes
        self.length = length
        self.vision_type = vision_type
        self.direction = Direction.UP
        self.body = self._create_snake()
        self.bearing = self._get_bearing()
        self.tail_direction = self.get_tail_direction()
  
        # Vision
        head = self.body[-1]
        angle = self.bearing
        vision_max_length = None  
        self.full_vision = FullVision(game.grid, head, angle, vision_max_length, vision_mode)
        
        # Brain input
        self.X = self._compute_input()
        self.model = None
        self.Y = None
        
        # Stats
        self.score = 0
        self.lifespan = 0
                
        
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
            return Direction.RIGHT
        elif delta_i >= 0:
            return Direction.LEFT
        elif delta_j < 0:
            return Direction.DOWN
        else:
            return Direction.UP
    
    
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
       
    
    def _compute_input(self):
        
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
                
        return X
          
    
    def update_state(self):
        self.update_full_vision()
        self._compute_input()
        
    
        
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
        
        # Test if it grow
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
                        
        return True
        
    
    
    
    
    
    