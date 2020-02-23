# -*- coding: utf-8 -*-
# Created on Sun Feb 16 15:25:05 2020
# @author: arthurd



import pygame

from pysnake.enum import Direction
from pysnake import Game, Snake
from pysnake.ui import WindowGame



def main(board_size=(15, 15), 
         cell_size=20, 

         show_window=False,
         show_grid=False):
    
    # Create the game
    game = Game(board_size)
    # game.grid.set_wall((2, 2), (4, 2), (3, 2))
    
    if show_window is not None:
                    
        # Create a PyGame instance
        screen_size = (cell_size*(board_size[1]), cell_size*(board_size[0]))
        pygame_win = pygame.display.set_mode(screen_size)
        # Delay between each frames
        clock = pygame.time.Clock()
        
        # Create a window to visualize the game
        window_game = WindowGame(game, pygame_win, cell_size=cell_size)
        snake = game.snakes[0]

        # Run the game until the end
        show_vision = False
        run = True
        wait = True
        while run:
            # Draw the game
            window_game.draw(show_grid=show_grid, show_vision=show_vision)
            
            # Ellapsed time between two frames
            pygame.time.delay(1)
            clock.tick(10)
            
                        
            # -----------
            # Key Pressed
            # -----------            
            
            # Quit()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    quit()
        
            # Update the direction
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                snake.direction = Direction.UP
                wait = False
            elif keys[pygame.K_RIGHT]:
                snake.direction = Direction.RIGHT
                wait = False
            elif keys[pygame.K_DOWN]:
                snake.direction = Direction.DOWN
            elif keys[pygame.K_LEFT]:
                snake.direction = Direction.LEFT
                wait = False
                
            # Restart the game
            elif keys[pygame.K_r] or keys[pygame.K_SPACE]:
                game.restart()
                snake = game.snakes[0]
                wait = True
                
            # Show the vision
            elif keys[pygame.K_v]:
                show_vision = not show_vision
                
            # Show the grid
            elif keys[pygame.K_g]:
                show_grid = not show_grid
                
                
            # Always move the snake
            # ... and check if it is alive
            if not wait:
                is_alive = snake.move()
            
                # if not is_alive:
                #     game.restart()
                #     snake = game.snake
                #     wait = True






if __name__ == "__main__":
    
    # Global parameters
    BOARD_SIZE = (13, 13)
    CELL_SIZE = 50
    
    # Run
    main(BOARD_SIZE, 
         CELL_SIZE, 
         
         show_grid = True,
         show_window = True)







