# -*- coding: utf-8 -*-
# Created on Sun Feb 16 15:25:05 2020
# @author: arthurd



import pygame

from pysnake.enum import Direction
from pysnake import Game, Snake
from pysnake.ui import WindowGame


class GamePlayer:
    
    def __init__(self,
                 board_size=(15, 15), cell_size=20, 
                 show_grid=True):
        
        self.board_size = board_size
        self.cell_size = cell_size
        self.show_grid = show_grid


    def run(self):
        # Create the game
        game = Game(self.board_size)
        # game.grid.set_wall((2, 2), (4, 2), (3, 2))
           
        # Create a PyGame instance
        screen_size = (self.cell_size*(self.board_size[1]), 
                       self.cell_size*(self.board_size[0]))
        pygame_win = pygame.display.set_mode(screen_size)
        # Delay between each frames
        clock = pygame.time.Clock()
        
        # Create a window to visualize the game
        window_game = WindowGame(game, pygame_win, cell_size=self.cell_size)
        snake = Snake(game)
        game.add_snake(snake)
    
        # Run the game until the end
        show_vision = False
        run = True
        wait = False
        can_die = True
        run_ai = True
        while run:
            # Draw the game
            window_game.draw(show_grid=self.show_grid, show_vision=show_vision)
            
            # Ellapsed time between two frames
            pygame.time.delay(1)
            clock.tick(5)
        
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
            elif keys[pygame.K_r]:
                run_ai = True
                wait = False
            
            # Can die ?
            elif keys[pygame.K_d]:
                can_die = not can_die
            # Restart the game
            elif keys[pygame.K_SPACE]:
                game.restart()
                snake = game.snakes[0]
                wait = True
            # Show the vision
            elif keys[pygame.K_v]:
                show_vision = not show_vision
            # Show the grid
            elif keys[pygame.K_g]:
                self.show_grid = not self.show_grid
                
            # Always move the snake
            # ... and check if it is alive
            if not wait:
                if run_ai:
                    next_direction = snake.next_direction()
                    snake.direction = next_direction
                    print(next_direction)
                is_alive = snake.move()
            
                if not is_alive and can_die:
                    game.restart()
                    snake = Snake(game)
                    game.add_snake(snake)
                    wait = False
            






if __name__ == "__main__":
    
    # Global parameters
    BOARD_SIZE = (13, 13)
    CELL_SIZE = 50
    
    # Run
    my_game = GamePlayer(BOARD_SIZE, 
                           CELL_SIZE)
    
    my_game.run()







