# -*- coding: utf-8 -*-
# Created on Wed Feb 19 11:55:11 2020
# @author: arthurd


from pysnake.enum import Item


class Cell:
    
    def __init__(self, coord, item):
        self.coord = coord
        self.item = item
        self.name = item.name
        self.value = item.value
        
    def is_wall(self):
        return self.item is Item.WALL
        
    def is_empty(self):
        return self.item is Item.EMPTY
    
    def is_snake(self):
        return self.item is Item.SNAKE
        
    def is_apple(self):
        return self.item is Item.APPLE
    
    
    

class Grid:
    
    def __init__(self, shape, fill_value=Item.EMPTY):
        self.shape = shape
        self.values = self._init_grid(fill_value)

            
    def _init_grid(self, fill_value):
        # Get the height and width from the shape
        height, width = self.shape
        # Create the grid
        values = []
        for i in range(height):
            row = []
            for j in range(width):
                coord = (i, j)
                # Create an empty cell
                cell = Cell(coord, fill_value)
                row.append(cell)
            values.append(row)
        
        return values
    
    def add_wall_borders(self):
        height, width = self.shape
        for i in range(height):
            for j in range(width):
                if i == 0 or i == height - 1:
                    self[i, j] = Cell((i, j), Item.WALL)
                elif j == 0 or j == width - 1:
                    self[i, j] = Cell((i, j), Item.WALL)
        
    def pad(self, padding):
        # Increase the shape of 
        height, width = self.shape
        new_height, new_width = height + 2*padding[0], width + 2*padding[1]
        values = []
        for i in range(new_height):
            row = []
            for j in range(new_width):
                if (i > 0 and i < new_height - 1) and (j > 0 and j < new_width - 1):
                    cell = self[i-1, j-1]
                row.append(cell)
            values.append(row)
        
        # And update the grid
        self.values = values
        self.shape = (new_height, new_width) 
        
           
    # Shortcut to set an element in the grid at coord
    def set_wall(self, *coords):
        for coord in coords:
            self[coord] = Cell(coord, Item.WALL)
    
    def set_empty(self, *coords):
        for coord in coords:
            self[coord] = Cell(coord, Item.EMPTY)
    
    def set_apple(self, *coords):
        for coord in coords:
            self[coord] = Cell(coord, Item.APPLE)
        
    def set_snake(self, *coords):
        for coord in coords:
            self[coord] = Cell(coord, Item.SNAKE)
        
    def set_cell(self, *cells):
        for cell in cells:
            self[cell.coord] = cell
    
    
    # Check the type of a game cell
    def is_wall(self, cell):
        grid_cell = self[cell.coord]
        return grid_cell.is_wall()
            
    def is_empty(self, cell):
        grid_cell = self[cell.coord]
        return grid_cell.is_empty()

    def is_apple(self, cell):
        grid_cell = self[cell.coord]
        return grid_cell.is_apple()

    def is_snake(self, cell):
        grid_cell = self[cell.coord]
        return grid_cell.is_snake()
    
    
    def is_outside(self, cell):
        """
        Check if a cell is outside the grid.

        Parameters
        ----------
        cell : Cell
            Cell containing its coordinates, in (i, j) system.

        Returns
        -------
        bool
            True if the cell is outside the grid (height, width), False otherwise.
        """
        
        # Get the indices and shape
        height, width = self.shape
        i, j = cell.coord
        # Check the coordinates
        if (i < 0) or (j < 0) or (i >= height) or (j >= width):
            return True
        return False
        
            
    # Custom methods to make tasks easier
    def row(self, index):
        return self.values[index]
    
    def col(self, index):
        return [row[index] for row in self.values]
    
            
    def __getitem__(self, tuple_index):
        i, j = tuple_index
        return self.values[i][j]
    
    def __setitem__(self, tuple_index, value):
        i, j = tuple_index
        self.values[i][j] = value
    
    
    
    def __str__(self):
        height, width = self.shape
        grid = ""
        for i in range(height):
            row = "\n\t"
            for j in range(width):
                if self[i, j].is_wall():
                    row += "##"
                elif self[i, j].is_empty():
                    row += "  "
                elif self[i, j].is_apple():
                    row += " *"
                elif self[i, j].is_snake():
                    row += "[]"
            grid += row
        
        return grid
    
