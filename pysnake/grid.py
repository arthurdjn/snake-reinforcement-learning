# -*- coding: utf-8 -*-
# Created on Wed Feb 19 11:55:11 2020
# @author: arthurd


from pysnake.enum import Item


class Cell:
    """
    Define a cell of a grid.

    Attributes
    ----------
    coord: tuple(int, int)
        Coordinates (i, j) or (y, x) of the cell.
    item: pysnake.enum.Item
        Item in the cell.
    name: str
        Name of the item.
    value: int
        Value of the item.
    """
    
    def __init__(self, coord, item):
        self.coord = coord
        self.item = item
        self.name = item.name
        self.value = item.value
        
        
    def is_wall(self):
        """
        Checks if the cell contains a Wall item.

        Returns
        -------
        bool
            True if it contains a Wall item.
        """
        return self.item is Item.WALL
        
    
    def is_empty(self):
        """
        Checks if the cell contains an Empty item.

        Returns
        -------
        bool
            True if it contains an Empty item.
        """
        return self.item is Item.EMPTY
    
    def is_snake(self):
        """
        Checks if the cell contains a Snake item.

        Returns
        -------
        bool
            True if it contains a Snake item.
        """
        return self.item is Item.SNAKE
        
    def is_apple(self):
        """
        Checks if the cell contains an Apple item.

        Returns
        -------
        bool
            True if it contains an Apple item.
        """
        return self.item is Item.APPLE
    
    
    

class Grid:
    """
    Contains a grid of cells.
    
    Attributes
    ----------
    shape: tuple(int, int)
        Shape of the grid.
    values: list(list(pysnake.grid.Cell))
        Cells in the grid.
    """
    
    def __init__(self, shape, fill_value=Item.EMPTY):
        self.shape = shape
        self.values = self._init_grid(fill_value)

            
    def _init_grid(self, fill_value):
        """
        Create a grid filled with the same value.

        Parameters
        ----------
        fill_value : pysnake.enum.Item
            Default value in the grid.

        Returns
        -------
        values : list(list(pysnake.grid.Cell))
            Grid of cells.
        """
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
        """
        Add Wall item around the grid. This does not affect the shape.

        Returns
        -------
        None.
        """
        height, width = self.shape
        for i in range(height):
            for j in range(width):
                if i == 0 or i == height - 1:
                    self[i, j] = Cell((i, j), Item.WALL)
                elif j == 0 or j == width - 1:
                    self[i, j] = Cell((i, j), Item.WALL)
        
    def pad(self, padding):
        """
        Pad the grid of Empty items.

        Parameters
        ----------
        padding : tuple(int, int)
            Height and width padding.

        Returns
        -------
        None.
        """
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
        """
        Set Wall item(s) to the grid, at specified coordinates.

        Parameters
        ----------
        *coords : tuple(int, int)
            Coordinates in (i, j) format where to add a Wall item.

        Returns
        -------
        None.
        """
        for coord in coords:
            self[coord] = Cell(coord, Item.WALL)
    
    def set_empty(self, *coords):
        """
        Set Empty item(s) to the grid, at specified coordinates.

        Parameters
        ----------
        *coords : tuple(int, int)
            Coordinates in (i, j) format where to add an Empty item.

        Returns
        -------
        None.
        """
        for coord in coords:
            self[coord] = Cell(coord, Item.EMPTY)
    
    def set_apple(self, *coords):
        """
        Set Apple item(s) to the grid, at specified coordinates.

        Parameters
        ----------
        *coords : tuple(int, int)
            Coordinates in (i, j) format where to add an Apple item.

        Returns
        -------
        None.
        """
        for coord in coords:
            self[coord] = Cell(coord, Item.APPLE)
        
    def set_snake(self, *coords):
        """
        Set Snake item(s) to the grid, at specified coordinates.

        Parameters
        ----------
        *coords : tuple(int, int)
            Coordinates in (i, j) format where to add a Snake item.

        Returns
        -------
        None.
        """
        for coord in coords:
            self[coord] = Cell(coord, Item.SNAKE)
        
    def set_cell(self, *cells):
        """
        Set Cell(s) to the grid.

        Parameters
        ----------
        *cells : pysnake.grid.Cell
            Cell(s) to update on the grid.

        Returns
        -------
        None.
        """
        for cell in cells:
            self[cell.coord] = cell
    
    
    # Check the type of a game cell
    def is_wall(self, cell):
        """
        Checks if a grid's cell contains a Wall item.

        Parameters
        ----------
        cell : pysnake.grid.Cell
            Cell of the grid to check.

        Returns
        -------
        bool
            True if the cell contains a Wall item.
        """
        grid_cell = self[cell.coord]
        return grid_cell.is_wall()
            
    def is_empty(self, cell):
        """
        Checks if a grid's cell contains an Empty item.

        Parameters
        ----------
        cell : pysnake.grid.Cell
            Cell of the grid to check.

        Returns
        -------
        bool
            True if the cell contains an Empty item.
        """
        grid_cell = self[cell.coord]
        return grid_cell.is_empty()

    def is_apple(self, cell):
        """
        Checks if a grid's cell contains an Apple item.

        Parameters
        ----------
        cell : pysnake.grid.Cell
            Cell of the grid to check.

        Returns
        -------
        bool
            True if the cell contains an Apple item.
        """
        grid_cell = self[cell.coord]
        return grid_cell.is_apple()

    def is_snake(self, cell):
        """
        Checks if a grid's cell contains a Snake item.

        Parameters
        ----------
        cell : pysnake.grid.Cell
            Cell of the grid to check.

        Returns
        -------
        bool
            True if the cell contains a Snake item.
        """
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
        """
        Get a row from the grid.

        Parameters
        ----------
        index : int
            Grid's index of the row.

        Returns
        -------
        list(pysnake.grid.Cell)
            Row at index 'index'.
        """
        return self.values[index]
    
    
    def col(self, index):
        """
        Get a column from the grid.

        Parameters
        ----------
        index : int
            Grid's index of the column.

        Returns
        -------
        list(pysnake.grid.Cell)
            Column at index 'index'.
        """
        return [row[index] for row in self.values]
    
            
    def __getitem__(self, tuple_index):
        """
        Get a Grid's cell from coordinates.

        Parameters
        ----------
        tuple_index : tuple(int, int)
            Coordinates of the cell.

        Returns
        -------
        pysnake.grid.Cell
            Grid's cell at tuple_index coordinates.
        """
        i, j = tuple_index
        return self.values[i][j]
    
    
    def __setitem__(self, tuple_index, value):
        """
        Set a Grid's cell at specified coordinates.

        Parameters
        ----------
        tuple_index : tuple(int, int)
            Coordinates of the cell.
        value : pysnake.grid.Cell
            New cell to set at tuple_index coordinates.

        Returns
        -------
        None.
        """
        i, j = tuple_index
        self.values[i][j] = value
    
        
    def __str__(self):
        """
        Convert the grid in string elements, to display in the console.

        Returns
        -------
        str
            String grid.
        """
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
    
