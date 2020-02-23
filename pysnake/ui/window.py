# -*- coding: utf-8 -*-
# Created on Sun Feb 16 18:08:48 2020
# @author: arthurd

import pygame

from pysnake.enum import Item


class WindowGame:
    
    def __init__(self,
                 game,
                 pygame_win,
                 cell_size=50,
                 color_palette={"background": (25, 29, 38), 
                                "snake": (125, 129, 138),
                                "apple": (21, 73, 22),
                                "grid": (0, 0, 0),
                                "vision": (125, 125, 125)}
                 ):
        
        self.pygame_win = pygame_win
        
        self.game = game
        self.shape = game.shape
        self.cell_size = cell_size
        self.color_palette = color_palette
        
        
    def _draw_grid(self):
        color = self.color_palette["grid"]
        height, width = self.shape
        for row in range(height):
            pygame.draw.line(self.pygame_win, color, (0, row*self.cell_size), (width*self.cell_size, row*self.cell_size))
        for col in range(width):
            pygame.draw.line(self.pygame_win, color, (col*self.cell_size, 0), (col*self.cell_size, height*self.cell_size))

    def _draw_vision(self, show_grid=True):
        for snake in self.game.snakes:
            for num_vision, vision in enumerate(snake.full_vision):
                
                # Draw the visible_object
                # Padd the cell if the grid mode is active
                pad = 0
                if show_grid:
                    pad = 1
                    
                i, j = vision.visible_object.coord
                if  vision.visible_object.item is Item.APPLE:
                    color = (21, 103, 22)
                elif vision.visible_object.item is Item.SNAKE:
                    color = (73, 11, 12)
                else:
                    color = (17, 20, 25)
                pygame.draw.rect(self.pygame_win, color, 
                                 (j*self.cell_size + pad, i*self.cell_size + pad, 
                                  self.cell_size - pad, self.cell_size - pad)) 
                
                # Draw the vision
                color = self.color_palette['vision']
                # Draw the direction in white
                if num_vision == 0:
                    color = (255, 255, 255)
                if vision.visible_object.item is Item.APPLE:
                    color = (0, 255, 0)
                elif vision.visible_object.item is Item.SNAKE:
                    color = (255, 0, 0)
                
                center = vision.center.coord
                end_point = vision.end_point
                start_point = ((center[1] + .5)*self.cell_size, 
                               (center[0] + .5)*self.cell_size)
                end_point = ((end_point[1] +.5)*self.cell_size,
                             (end_point[0] + .5)*self.cell_size)
                
                pygame.draw.line(self.pygame_win, color, start_point, end_point)
                                             
                # TEST ONLY
                # check if the interpolation is correct, visualize the end_point grid cell
                # i, j = round(vision.end_point[0]), round(vision.end_point[1])
                # color = (255, 20, 25)
                # pygame.draw.rect(self.pygame_win, color, 
                #                  (j*self.cell_size + pad, i*self.cell_size + pad, 
                #                   self.cell_size - pad, self.cell_size - pad)) 
                
            
    def _draw_game(self):
        # Get the parameters
        game = self.game
        grid = game.grid
        height, width = grid.shape
                            
        # Draw the grid
        for i in range(height):
            for j in range(width):
                
                # If the cell is a wall
                if grid[i, j].is_wall():
                    color = (0, 0, 0)
                    pygame.draw.rect(self.pygame_win, color, 
                                     (j*self.cell_size, i*self.cell_size, 
                                      self.cell_size, self.cell_size))  
                
                # If the cell is the background
                elif grid[i, j].is_empty():
                    color = self.color_palette['background']
                    pygame.draw.rect(self.pygame_win, color, 
                                     (j*self.cell_size, i*self.cell_size, 
                                      self.cell_size, self.cell_size))  

                # If the cell is the snake
                elif grid[i, j].is_snake():
                    color = self.color_palette['snake']
                    pygame.draw.rect(self.pygame_win, color, 
                                     (j*self.cell_size, i*self.cell_size, 
                                      self.cell_size, self.cell_size))  

                # If the cell is the apple
                elif grid[i, j].is_apple():
                    color = self.color_palette['apple']
                    pygame.draw.rect(self.pygame_win, color, 
                                     (j*self.cell_size, i*self.cell_size, 
                                      self.cell_size, self.cell_size)) 
            
            
            
        
    def draw(self, show_grid=True, show_vision=False):

        self._draw_game()
        
        if show_grid:
            self._draw_grid()

        
        if show_vision:
            self._draw_vision(show_grid)

                
        pygame.display.update()


