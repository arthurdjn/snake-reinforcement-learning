# -*- coding: utf-8 -*-
# Created on Wed Feb 19 13:36:39 2020
# @author: arthurd


from pysnake import Item, Cell, Grid




def test_Cell():
    cell_empty = Cell((0, 0), Item.EMPTY)
    cell_apple = Cell((1, 1), Item.APPLE)
    cell_snake = Cell((0, 2), Item.SNAKE)
    print("\t1/ Cell empty :", cell_empty.coord, cell_empty.item, cell_empty.name)
    print("\t2/ Cell apple :", cell_apple.coord, cell_apple.item, cell_apple.name)
    print("\t3/ Cell snake :", cell_snake.coord, cell_snake.item, cell_snake.name)



def test_Grid():
    shape = (10, 10)
    grid = Grid(shape)   
    index = (2, 2)
    cell = grid[index]
    row = grid.row(2)
    row = [cell.name for cell in row]
    print("Grid shape is", grid.shape)
    print("\t2/ Grid item at {0} is {1}".format(index, cell.name))
    print("\t3/ Row cells names at index 2 is", row)
    print("\t4/ Set apple at (2, 3)")
    
    print("\t5/ Set snake at (5, 5), (6, 5), (6, 5)")
    apple = Cell((2, 3), Item.APPLE)
    snake1 = Cell((5, 5), Item.SNAKE)
    snake2 = Cell((6, 5), Item.SNAKE)
    snake3 = Cell((7, 5), Item.SNAKE)

    grid.set_cell(apple)
    grid.set_cell(snake1, snake2, snake3)
    print(grid)
    
    print("\t6/ Adding walls")
    grid.add_wall_borders()
    print(grid)


if __name__ == "__main__":
    

    # Test Cell
    print("Testing Cell...")
    test_Cell()
    print("Cell tested.")
    
    
    # Test Grid
    print("Testing Grid...")
    test_Grid()
    print('Grid tested.')
    
    
    