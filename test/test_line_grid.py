# -*- coding: utf-8 -*-
# Created on Thu Feb 20 10:46:04 2020
# @author: arthurd

import matplotlib.pyplot as plt
import numpy as np


# Pretti graphs
plt.style.use('seaborn-darkgrid')


def plotLineLow(center, end_point):
    
    
    i_center, j_center = center
    i_end, j_end = end_point
    delta_j = j_end - j_center
    delta_i = i_end - i_center
    step_i = 1
    
    points = []
    
    if delta_i < 0:
        step_i = -1
        delta_i = -delta_i
    D = 2*delta_i - delta_j
    i = i_center
    
    for j in range(j_center, j_end+1):
        points.append((i, j))
        if D > 0:
               i = i + step_i
               D = D - 2*delta_j
        D = D + 2*delta_i
        
    return points



def plotLineHigh(center, end_point):
    
    i_center, j_center = center
    i_end, j_end = end_point
    delta_j = j_end - j_center
    delta_i = i_end - i_center
    step_j = 1
    
    points = []
    
    if delta_j < 0:
        step_j = -1
        delta_j = -delta_j
    D = 2*delta_j - delta_i
    j = j_center

    for i in range(i_center, i_end+1):
        points.append((i, j))
        if D > 0:
               j = j + step_j
               D = D - 2*delta_i
        D = D + 2*delta_j
        
    return points


def plotLine(center, end_point):
    
    i_center, j_center = center
    i_end, j_end = end_point
    points = None
    if abs(i_end - i_center) < abs(j_end - j_center):
        if j_center > j_end:
            # points = plotLineLow(end_point, center)
            points = plotLineLow(end_point, center)
            points.reverse()
            
        else:
            print('ooo')
            points = plotLineLow(center, end_point)
    else:
        if i_center > i_end:
            print("prout")
            points = plotLineHigh(end_point, center)
            points.reverse()
        else:
            print("ok")
            points =  plotLineHigh(center, end_point)
    
    return points[1:]


def line_grid(j_center, i_center, j_end, i_end):
    delta_j = j_end - j_center
    delta_i = i_end - i_center
    D = 2*delta_i - delta_j
    i = i_center
    
    points = []
    for j in range(j_center, j_end+1):
        points.append((i, j))
        if D > 0:
            i = i + 1
            D = D - 2*delta_j
        D = D + 2*delta_i
    return points
        
        



def test_line_grid():
    # Parameters
    center = (5, 0)
    end_point = (0, 0)
    
    # ------------------------------
    # Testing and visualizing vision
    # ------------------------------
    
    # Matplotlib figures
    fig, ax = plt.subplots(1, 1)

    points = plotLine(center, end_point)
    
    print(points)
    
    X = [p[1] for p in points]
    Y = [p[0] for p in points]
    
    # Subplot
    # Plot the vision
    draw_vision = [[center[0], end_point[0]], [center[1], end_point[1]]]
    ax.plot(draw_vision[1], draw_vision[0], color="skyblue", label="vision")
    # Plot visible cells / origin / end_point
    ax.scatter(X, Y, zorder=10, color="darkcyan", label="visible cells")
    
    # Frame and grid
    ax.legend(loc=0, frameon=True)
    ax.set_ylim(10, 0)
    ax.set_xlim(0, 10)
    x_ticks = np.arange(0, 10, 1)
    y_ticks = np.arange(0, 10, 1)
    ax.set_xticks(x_ticks)
    ax.set_yticks(y_ticks)
                

    # Small margins
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    
    print(points)



if __name__ == "__main__":
    
    test_line_grid()
