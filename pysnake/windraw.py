# -*- coding: utf-8 -*-
# Created on Sun Feb 16 18:08:48 2020
# @author: arthurd


# Import pygame if installed.
# If not, it is still possible to train the model but without visualization.
try:
    import pygame
    from pygame import gfxdraw
except ModuleNotFoundError:
    print("Module PyGame is not installed.")

# Useful packages
import numpy as np
# PySnake modules
from pysnake.enum import Item



class WindowGame:
    """
    PySnake window, depends on pygame.
    
    Attributes
    ----------
    game : pysnake.game.Game
        Main game.
    pygame_win : pygame.display
        The pygame window.
    cell_size : int, optional
        Size of a pysnake's cell. The default is 50.
    bbox_game : tuple(int, int), optional
        Top-left position of the game display. The default is (0, 0).
    bbox_network : tuple(int, int), optional
        Top-left position of the network display. The default is (0, 0).
    color_palette: dict
        Colors used to draw all elements.
    """
    
    def __init__(self, game, pygame_win,
                 cell_size = 50, 
                 bbox_game = (500, 500, 500, 500), 
                 bbox_network = (0, 0, 500, 500)):
        
        self.pygame_win = pygame_win
        self.game = game
        self.cell_size = cell_size
        self.bbox_game = bbox_game
        self.bbox_network = bbox_network
        self.color_palette = {"background":     (255, 255, 255),
                              "empty":          (37, 54, 69),
                              "wall":           (32, 44, 55),
                              "snake":          (46, 142, 212),
                              "snake_head":     (46, 142, 212),
                              "apple":          (227, 68, 52),
                              "neuron":         (255, 255, 255),
                              "weight_pos":     (37, 117, 50),
                              "weight_neg":     (227, 68, 52),
                              "visible_snake":  (44, 112, 155),
                              "visible_apple":  (237, 37, 27),
                              "visible_wall":   (19, 28, 35),
                              "vision":         (102, 119, 132),
                              "vision_apple":   (237, 37, 27),
                              "vision_snake":   (255, 0, 0)}
        

    def _draw_vision(self):
        """
        Draw the full vision sensor for all snakes in the game.

        Returns
        -------
        None.
        """
        j0, i0, _, _ = self.bbox_game
        # Draw the vision for all snakes
        for snake in self.game.snakes:
            for num_vision, vision in enumerate(snake.full_vision):
                
                # Draw the first_visible_item
                first_visible_item = vision.nearest_cells[0]
                i, j = first_visible_item.coord
                if  first_visible_item.item is Item.APPLE:
                    color = self.color_palette['visible_apple']
                elif first_visible_item.item is Item.SNAKE:
                    color = self.color_palette['visible_snake']
                else:
                    color = self.color_palette['empty']
                pygame.draw.rect(self.pygame_win, color, 
                                 (j0 + j * self.cell_size, i0 + i * self.cell_size, 
                                  self.cell_size, self.cell_size)) 
                
                # Set the vision's color regarding the visible object
                color = self.color_palette['vision']
                if first_visible_item.item is Item.APPLE:
                    color = self.color_palette['vision_apple']
                elif first_visible_item.item is Item.SNAKE:
                    color = self.color_palette['vision_snake']
                
                # Draw a line from the center to the last object (usually wall)
                center = vision.center.coord
                end_point = vision.end_point
                start_point = (j0 + (center[1] + .5)*self.cell_size, 
                               i0 + (center[0] + .5)*self.cell_size)
                end_point = (j0 + (end_point[1] +.5)*self.cell_size,
                             i0 + (end_point[0] + .5)*self.cell_size)
                pygame.draw.line(self.pygame_win, color, start_point, end_point)

            
    def _draw_game(self, show_grid):
        """
        Draw the game's grid.

        Parameters
        ----------
        show_grid : bool
            Draw a grid.

        Returns
        -------
        None.
        """
        # Get the parameters
        game = self.game
        grid = game.grid
        height, width = grid.shape
        j0, i0, _, _ = self.bbox_game
        
        # Draw the grid
        for i in range(height):
            for j in range(width):
               
                # If the cell is a wall
                if grid[i, j].is_wall():
                    color = self.color_palette['wall']
                    pygame.draw.rect(self.pygame_win, color, 
                                     (j0 + j * self.cell_size, i0 + i * self.cell_size, 
                                      self.cell_size, self.cell_size))  
               
                # If the cell is the background
                elif grid[i, j].is_empty():
                    color = self.color_palette['empty']
                    if show_grid and ((i +j)%2 == 1):
                        color = self.color_palette['wall']
                    pygame.draw.rect(self.pygame_win, color, 
                                     (j0 + j * self.cell_size, i0 + i * self.cell_size, 
                                      self.cell_size, self.cell_size))  
                
                # If the cell is the snake
                elif grid[i, j].is_snake():
                    color = self.color_palette['snake']
                    pygame.draw.rect(self.pygame_win, color, 
                                     (j0 + j * self.cell_size, i0 + i * self.cell_size, 
                                      self.cell_size, self.cell_size))  
                
                # If the cell is the apple
                elif grid[i, j].is_apple():
                    color = self.color_palette['apple']
                    pygame.draw.rect(self.pygame_win, color, 
                                     (j0 + j * self.cell_size, i0 + i * self.cell_size, 
                                      self.cell_size, self.cell_size))  
       
        # Draw the snakes head
        for snake in self.game.snakes:
            i, j = snake.body[-1].coord
            color = self.color_palette['snake_head']
            pygame.draw.rect(self.pygame_win, color, 
                            (j0 + j * self.cell_size, i0 + i * self.cell_size, 
                             self.cell_size, self.cell_size))   
            
    
    def _draw_neurons(self):
        """
        Draw neurons of the last added snake to the game.

        Returns
        -------
        None.
        """
        # Origin on where to draw the network
        j0, i0, width, height = self.bbox_network
        color = self.color_palette["neuron"]
        
        # Neural Network
        snake = self.game.snakes[-1]
        layers_dimension = snake.nn_layers_dimension
        num_layers = len(layers_dimension)
        max_neurons = max(layers_dimension)
        
        # Layers margin
        layer_spacing = width // num_layers
        padding = 20
        neuron_spacing = int((height - 2 * padding)/ max_neurons)
        neuron_radius = int(neuron_spacing / 2 * 0.6)
        
        # Margin from one layer to the next one
        j = j0 + layer_spacing // 2
        for num_layer, layer in enumerate(layers_dimension):
            # Center the neurons y-axis
            margin_top = int(neuron_spacing * (max_neurons - layer + 1.5) / 2) + padding // 2
            A = snake.nn_params['A_' + str(num_layer)]
            A = A.reshape(A.size)
            # Do not divide by 0 when normalizing !
            A = np.divide(np.abs(A), np.max(A), 
                          out=np.zeros_like(A), 
                          where=np.max(A)!=0)
            
            for i in range(layer):
                # Draw the neurons regarding its activation
                color_neuron = (int(color[0] * A[i]), int(color[1] * A[i]), int(color[2] * A[i]))
                gfxdraw.filled_circle(self.pygame_win, j, margin_top + i0 + i * neuron_spacing, 
                               neuron_radius, color_neuron)
                # Neuron border
                gfxdraw.aacircle(self.pygame_win, j, margin_top + i0 + i * neuron_spacing, 
                               neuron_radius, (40, 50, 60))
            # Switch to another layer
            j += layer_spacing
            
    
    def _draw_weights(self):
        """
        Draw weights of the last added snake to the game.

        Returns
        -------
        None.
        """
        # Origin on where to draw the network
        j0, i0, width, height = self.bbox_network
       
        # Neural Network
        snake = self.game.snakes[-1]
        layers_dimension = snake.nn_layers_dimension
        num_layers = len(layers_dimension)
        max_neurons = max(layers_dimension)
        
        # Layer margin
        layer_margin = width // num_layers
        padding = 20
        neuron_spacing = int((height - 2 * padding)/ max_neurons)
        
        # Margin from one layer to the next one
        layer_spacing = j0 + layer_margin // 2
        for num_layer in range(len(layers_dimension) - 1):
            # Get the dimension of the layers
            layer_start = layers_dimension[num_layer]
            layer_end = layers_dimension[num_layer + 1]
            # Center the neurons y-axis
            margin_top_start = int(neuron_spacing * (max_neurons - layer_start + 1.5) / 2) + padding // 2
            margin_top_end = int(neuron_spacing * (max_neurons - layer_end + 1.5) / 2) + padding // 2
           
            # Get the weights / shape
            W = snake.nn_params['W_' + str(num_layer + 1)]
            N, M = W.shape
            # Draw a line for each weights
            for i in range(N):
                for j in range(M):
                    start = (layer_spacing, margin_top_start + i0 + i * neuron_spacing)
                    end = (layer_spacing + layer_margin, margin_top_end + j0 + j * neuron_spacing)
                    
                    # Different colors regarding weight sign
                    if W[i, j] > 0:
                        color = self.color_palette["weight_pos"]
                    else:
                        color = self.color_palette["weight_neg"] 
                    
                    # Draw the neurons connection from layer_start to layer_end
                    pygame.draw.line(self.pygame_win, color, start, end)
            
            # Move to another set of layers
            layer_spacing += layer_margin
            
        
    def draw(self, show_grid=True, show_vision=False):
        """
        Draw and update the pygame window.

        Parameters
        ----------
        show_grid : bool, optional
            Show the grid if true. The default is True.
        show_vision : bool, optional
            Show the snakes vision if true. The default is False.

        Returns
        -------
        None.
        """
        
        # Draw the background
        height, width = pygame.display.get_surface().get_size()
        color = self.color_palette["background"]
        pygame.draw.rect(self.pygame_win, color, 
                                     (0, 0, width, height))  
        
        # Draw the components
        self._draw_game(show_grid)
        if show_vision:
            self._draw_vision()    
        self._draw_weights()
        self._draw_neurons()
    
        # Update !
        pygame.display.update()


