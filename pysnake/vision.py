# -*- coding: utf-8 -*-
# Created on Sun Feb 16 22:19:14 2020
# @author: arthurd



import numpy as np

from pysnake.enum import Item
from pysnake.grid import Cell

from pysnake.utils import one_hot_vector



class Vision:
    
    def __init__(self, grid, center, angle=0, max_length=None):
        
        # Vision in a grid !
        self.grid = grid
                
        self.angle = angle % 360 # Get the modulo [360], for convenience
        self.max_length = max_length
        self.center = center
        self.end_point = self._get_end_point()
        self.end_cell = self.grid[int(self.end_point[0]), int(self.end_point[1])]
        
        
        # Visibe item from its vision
        self.visible_object = self.detect()[0]
        self.nearest_cells = self.detect()
        
        # Distances vector : distance from the walls, to apple, to itself
        # self.distances = self.to_distances()     
        
    
    def _get_end_point(self):
        """
        Get the last point seen from the vision center.
        In other words, it will compute the point coordinates that intersect the grid borders.

        Returns
        -------
        end_point : tuple
            End point coordinates seen from center in the grid.
        """
        
        # Params
        i, j = self.center.coord
        height, width = self.grid.shape
        angle = self.angle
        angle_rad = np.deg2rad(angle)
        # Get the last point seen by vision
        end_point = None
        
        # Check the first quarter of the trigonometric circle
        if angle == 0:
            end_point = (0, j)
        elif angle < 90:
            j_end = j - np.tan(angle_rad) * (i)
            i_end = i - np.tan(np.pi/2 - angle_rad) * (j)
            
            # Avoid issues with float numbers...
            i_end, j_end = round(i_end, ndigits=12), round(j_end, ndigits=12)
            # If i_end <= i - i0, 
            # it means that the ray will it the left side of the grid
            if 0 <= i_end <= i:
                end_point = (i_end, 0)
            else:
                end_point = (0, j_end)
                
        # Second quarter
        elif angle == 90:
            end_point = (i, 0)
        elif angle < 180:
            j_end = j - np.tan(np.pi - angle_rad) * (height-1 - i)
            i_end = i + np.tan(angle_rad - np.pi/2) * j
            
            # Avoid issues with float numbers...
            i_end, j_end = round(i_end, ndigits=12), round(j_end, ndigits=12)
            if i <= i_end <= height-1:
                end_point = (i_end, 0)
            else:
                end_point = (height - 1, j_end)
                
        # Third quarter
        elif angle == 180:
            end_point = (height-1, j)
        elif angle < 270:
            j_end = j + np.tan(angle_rad - np.pi) * (height-1 - i)
            i_end = i + np.tan(3*np.pi/2 - angle_rad) * (width-1 - j)
            
            # Avoid issues with float numbers...
            i_end, j_end = round(i_end, ndigits=12), round(j_end, ndigits=12)
            if i <= i_end <= height-1:
                end_point = (i_end, width - 1)
            else:
                end_point = (height - 1, j_end)    
                
        # Last quarter
        elif angle == 270:
            end_point = (i, width-1)
        else:
            j_end = j + np.tan(2*np.pi - angle_rad) * i
            i_end = i - np.tan(angle_rad - 3*np.pi/2) * (width-1 -  j)

            # Avoid issues with float numbers...
            i_end, j_end = round(i_end, ndigits=12), round(j_end, ndigits=12)            
            if 0 <= i_end <= i:
                end_point = (i_end, width - 1)
            else:
                end_point = (0, j_end)  
              
        return end_point


    def look(self):
        # print("WARNING:\nThis method is deprecated, use vision.look() instead.")
        # Star and end points
        start_i, start_j = self.center.coord
        end_i, end_j = self.end_point
        # End point seen on the grid system
        end_i, end_j = int(round(end_i)), int(round(end_j))
        
        # Know wich direction to draw the line
        delta_i = abs(end_i - start_i)
        delta_j = abs(end_j - start_j)        
        sign_j = np.sign(end_j - start_j)
        sign_i = np.sign(end_i - start_i)
            
        err = delta_i - delta_j
        
        # Collect the cells visible from the starting point
        visible_cells = []       
        while (start_i != end_i or start_j != end_j):

            e2 = 2 * err
            if e2 >= - delta_j:
                # overshot in the y direction
                err = err - delta_j
                start_i = start_i + sign_i               
                # cell = self.grid[start_i, start_j]
                # visible_cells.append(cell)
                
            if e2 <= delta_i:
                # overshot in the x direction
                err = err + delta_i
                start_j = start_j + sign_j
                # cell = self.grid[start_i, start_j]
                # visible_cells.append(cell)
                
            cell = self.grid[start_i, start_j]
            visible_cells.append(cell)

        return visible_cells
            
    
    def detect(self):
        visible_cells = self.look()
        # Keep the first object of each class
        nearest_cells = []
        has_seen_object = np.full(len(Item) - 1, False)
        for cell in visible_cells:
            if not cell.is_empty():
                # Is the class cell already be seen ?
                if has_seen_object[cell.value] == False:
                    has_seen_object[cell.value] = True
                    nearest_cells.append(cell)
                # Return cell containing first visible object
        return nearest_cells
                
        
    def to_binary(self):
        # One-hot encoded vision
        # Ignore empty cell
        num_class = len(Item) - 1
        binary_vision = np.zeros(num_class)
        for cell in self.nearest_cells:
            binary_vision[cell.value] = 1
        return binary_vision
        
    
    def to_distances(self):
        # Ditance to walls | Distance to Apple | Distance to itself | etc.
        # Ignore empty cell
        num_class = len(Item) - 1
        distance_vision = np.zeros(num_class)
        for cell in self.nearest_cells:
            distance_vector = (self.center.coord[0] - cell.coord[0],
                               self.center.coord[1] - cell.coord[1])
            distance = np.linalg.norm(distance_vector)
            distance_vision[cell.value] = distance
        
        return distance_vision
        
           
    
class FullVision:
    
    def __init__(self, grid, center, bearing, max_length=None, mode=8):
        
        self.grid = grid
        
        self.mode = mode
        self.center = center
        self.max_length = max_length
        self.bearing = bearing
        
        self.visions = self._init_visions(self.bearing)
        
                
    def _init_visions(self, bearing):
               
        visions = []
        mode = self.mode
        # Create n_mode vision objects, with an equal angle theta from each other
        theta = 360 / mode
        angle = bearing
        for i in range(mode):
            vision = Vision(self.grid, self.center, angle, self.max_length)
            visions.append(vision)
            # Rotate the next vision
            angle += theta
            
        return visions
            
    
    def update(self, center, bearing):
        self.center = center
        self.bearing = bearing
        self.visions = self._init_visions(bearing)
    
    
    def __getitem__(self, index):
        return self.visions[index]
    
    def __setitem__(self, index, value):
        self.visions[index] = value
    
    
    