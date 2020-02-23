# -*- coding: utf-8 -*-
# Created on Mon Feb 17 13:28:08 2020
# @author: arthurd


import matplotlib.pyplot as plt
import numpy as np


# Import PySnake modules
from pysnake.utils import cell_to_coord
from pysnake import Grid
from pysnake import Vision, FullVision

# Pretty graphs
plt.style.use('seaborn-darkgrid')




def test_get_end_point():
    
    # Parameters
    shape = (10, 10)
    grid = Grid(shape)
    center = (5, 0)
    angle = 0
    max_length = None    
    
    # ------------------------------
    # Testing and visualizing vision
    # ------------------------------

    # Get the bbox grid shape
    height, width = grid.shape
    
    # Matplotlib figures
    fig, axs = plt.subplots(2, 2)
    # Set the suptitle
    fig.suptitle("Testing Vision._get_end_point() at modulo [{0}°]".format(angle))
    # Creating 4 subgraphs
    fig_num = 1
    for i in range(2):
        for j in range(2):
            # Create the vision from center and angle
            vision = Vision(grid, center, angle, max_length)
            end_point = vision._get_end_point()  
            end_cell = (int(end_point[0]), int(end_point[1]))
            # Check the results
            print("\t{}/ End point n°{} : {}".format(fig_num, (i, j), end_point))
            print("\t   End cell  n°{} : {}".format(i+j, end_cell))
            
            # Get the vision direction
            X = [center[1], end_point[1]]
            Y = [center[0], end_point[0]]
            
            # Subplot
            ax = axs[i, j]
            ax.plot(X, Y, color="skyblue", label="vision")
            ax.scatter(end_point[1], end_point[0], color="skyblue", zorder=10, label="vision end_point")
            ax.scatter(end_cell[1], end_cell[0], color="steelblue", zorder=8, label="vision end_cell")
            ax.scatter(center[1], center[0], color="mediumvioletred", zorder=10, label="vision origin")
            
            # Frame and grid
            ax.legend(loc=0, frameon=True)
            ax.set_ylim(height, 0)
            ax.set_xlim(0, width)
            x_ticks = np.arange(0, width, 1)
            y_ticks = np.arange(0, height, 1)
            ax.set_xticks(x_ticks)
            ax.set_yticks(y_ticks)
            
            # Rotate the vision
            angle += 90
            
            # Update the figure index (for the plot / console log)
            fig_num += 1
    
    # Small margins
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])

   
    
def test_look():
    # Parameters
    shape = (10, 10)
    grid = Grid(shape)
    center = (6, 5)
    angle = 30
    max_length = None    

    # ------------------------------
    # Testing and visualizing vision
    # ------------------------------

    # Get the bbox grid shape
    height, width = grid.shape
    
    # Matplotlib figures
    fig, axs = plt.subplots(2, 2)
    fig.suptitle("Testing Vision.look()")
    fig_num = 1
    for i in range(2):
        for j in range(2):
            # Create the vision from center and angle
            vision = Vision(grid, center, angle, max_length)
            visible_cells = vision.look() 
            # Get the coordinates from the cells
            coords = cell_to_coord(*visible_cells)
            print("\t{}/ visible_cells n°{} : \n{}".format(fig_num, (i, j), coords))
            # (i, j) != (x, y)
            X = [cell[1] for cell in coords]
            Y = [cell[0] for cell in coords]
            
             # Subplot
            ax = axs[i, j]
            # Plot the vision
            draw_vision = [[center[0], vision.end_point[0]], [center[1], vision.end_point[1]]]
            ax.plot(draw_vision[1], draw_vision[0], color="skyblue", label="vision")
            # Plot visible cells / origin / end_point
            ax.scatter(vision.end_point[1], vision.end_point[0], zorder=10, color="skyblue", label="vision end_point")
            ax.scatter(X, Y, color="steelblue", label="vision point")
            ax.scatter(center[1], center[0], zorder=10, color="mediumvioletred", label="vision origin")
            
            # Frame and grid
            ax.legend(loc=0, frameon=True)
            ax.set_ylim(height, 0)
            ax.set_xlim(0, width)
            x_ticks = np.arange(0, width, 1)
            y_ticks = np.arange(0, height, 1)
            ax.set_xticks(x_ticks)
            ax.set_yticks(y_ticks)
            
            # Rotate the vision for next graph
            angle += 90
            
            # Update the figure index (for the plot / console log)
            fig_num += 1
    
    # Small margins
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    
    
    
def test_detect():
    # Parameters
    shape = (10, 10)
    grid = Grid(shape)
    center = (6, 5)
    angle = 45
    max_length = None    

    # ------------------------------
    # Testing and visualizing vision
    # ------------------------------

    # Get the bbox grid shape
    height, width = grid.shape
    
    # Set some item in the grid
    grid.set_apple((1, 0))
    grid.set_snake((9, 8))
    
    # Matplotlib figures
    fig, axs = plt.subplots(2, 2)
    fig.suptitle("Testing Vision.detect_item()")
    fig_num = 1
    for i in range(2):
        for j in range(2):
            # Create the vision from center and angle
            vision = Vision(grid, center, angle, max_length)
            visible_object = vision.visible_object
            visible_object_coord = visible_object.coord
            # Get the coordinates from the cells
            print("\t{}/ Visible item at {} : {}".format(fig_num, visible_object.coord, visible_object.name))
            
             # Subplot
            ax = axs[i, j]
            # Plot the vision
            draw_vision = [[center[0], vision.end_point[0]], [center[1], vision.end_point[1]]]
            ax.plot(draw_vision[1], draw_vision[0], color="skyblue", label="vision")
            # Plot visible cells / origin / end_point
            ax.scatter(visible_object_coord[1], visible_object_coord[0], zorder=10, color="darkcyan", label="item")
            ax.scatter(center[1], center[0], zorder=10, color="mediumvioletred", label="vision origin")
            
            # Frame and grid
            ax.legend(loc=0, frameon=True)
            ax.set_ylim(height, 0)
            ax.set_xlim(0, width)
            x_ticks = np.arange(0, width, 1)
            y_ticks = np.arange(0, height, 1)
            ax.set_xticks(x_ticks)
            ax.set_yticks(y_ticks)
            
            # Rotate the vision for next graph
            angle += 90
            
            # Update the figure index (for the plot / console log)
            fig_num += 1
    
    # Small margins
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    
    

def test_full_vision():
    # Parameters
    shape = (10, 10)
    grid = Grid(shape)
    center = (6, 5)
    bearing = 0
    mode = 8
    max_length = None    

    # ------------------------------
    # Testing and visualizing vision
    # ------------------------------

    # Get the bbox grid shape
    height, width = grid.shape
    
    # Set some item in the grid
    grid.set_apple((1, 0))
    grid.set_snake((9, 8))
    
    # Matplotlib figures
    fig, ax = plt.subplots(1, 1)
    fig.suptitle("Testing FullVision.visions")

    # Create the vision from center and angle
    full_vision = FullVision(grid, center, bearing, max_length, mode)
    
    for vision in full_vision.visions:
        end_point = vision.end_point
        # Plot the vision
        draw_vision = [[center[0], end_point[0]], [center[1], end_point[1]]]
        ax.plot(draw_vision[1], draw_vision[0], color="skyblue")
        # Plot visible cells / origin / end_point
        ax.scatter(center[1], center[0], zorder=10, color="mediumvioletred")
    
    # Frame and grid
    ax.set_ylim(height, 0)
    ax.set_xlim(0, width)
    x_ticks = np.arange(0, width, 1)
    y_ticks = np.arange(0, height, 1)
    ax.set_xticks(x_ticks)
    ax.set_yticks(y_ticks)
        
    # Small margins
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])    
    
    
    

if __name__ == "__main__":
   
    # # Test end point
    # print("Testing Vision._get_end_point()...")
    # test_get_end_point()
    # print("Vision._get_end_point() tested.")
    
    
    # Test look
    print("\nTesting Vision.look()...")
    test_look()
    print("Vision.look() tested.")
    
    
    # # Test detect
    # print("\nTesting Vision.detect()...")
    # test_detect()
    # print("Vision.detect() tested.")
    
    
    # # Test FullVision
    # print("\nTesting FullVision.visions...")
    # test_full_vision()
    # print("FullVision.visions tested.")
    
    
    
    
    
    
    
    
    