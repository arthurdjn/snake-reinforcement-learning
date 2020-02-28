# -*- coding: utf-8 -*-
# Created on Sun Feb 16 15:25:05 2020
# @author: arthurd



import pygame
import matplotlib.pyplot as plt

from pysnake.enum import Direction
from pysnake import Game, Snake
from pysnake.ui import WindowGame

from pysnake.gen import Population, Individual, Chromosome

from math import sqrt
import random as rd

NUM_INDIVIDUALS = 60
NUM_GENERATIONS = 100
BOARD_SIZE = (15, 15)


# -*- coding: utf-8 -*-
# Created on Sun Feb 16 15:25:05 2020
# @author: arthurd



import pygame

from pysnake.enum import Direction
from pysnake import Game, Snake
from pysnake.ui import WindowGame


class GameEvolution:
    
    def __init__(self,
                 board_size=(15, 15), cell_size=20,
                 epochs=3000, num_population=1500):
        
        self.board_size = board_size
        self.cell_size = cell_size
        screen_size = (self.cell_size*(self.board_size[1]), 
                       self.cell_size*(self.board_size[0]))
        self.pygame_win = pygame.display.set_mode(screen_size)
        self.clock = pygame.time.Clock()
        self.game = Game(self.board_size)
        self.window_game = WindowGame(self.game, self.pygame_win, cell_size=self.cell_size)
        self.num_population = num_population
        self.epochs = epochs


    def play(self, snake=None):
        # Create the game
        if snake is None:
            snake = Snake(self.game)
            self.game.add_snake(snake)
    
        # Run the game until the end
        is_alive = True
        while is_alive:
            # Draw the game
            self.window_game.draw(show_grid=True, show_vision=False)
            
            # Ellapsed time between two frames
            pygame.time.delay(1)
            self.clock.tick(5)
               
            # Quit()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    quit()
            # Update the direction
            next_direction = snake.next_direction()
            snake.direction = next_direction
            print(next_direction)
            is_alive = snake.move()
            
            if not is_alive:
                self.game.restart()
                self.play()


    def evolve(self):
        
        # Pygame       
        # Create a window to visualize the game
       
        fitness = []  # For tracking average fitness over generation
        
        # Create and initialize the population
        individuals = [Snake(self.game) for _ in range(self.num_population)]                
        pop = Population(individuals)
              
        for generation in range(self.epochs):
            
            for i in range(self.num_population):
                chromosomes = pop.individuals[i].chromosomes
                snake = Snake(self.game, chromosomes=chromosomes)
                self.game.add_snake(snake)
                self.game.add_apple()
                snake.update_full_vision()
                # Run the game until the end
                is_alive = True
                while is_alive:
                    # Draw the game
                    self.window_game.draw(show_grid=True, show_vision=False)
                    
                    # Ellapsed time between two frames
                    pygame.time.delay(1)
                    self.clock.tick(50)   
                    # Quit()
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            quit()
                    # Update the direction
                    next_direction = snake.next_direction()
                    snake.direction = next_direction
                    is_alive = snake.move()
                    if not is_alive:
                        self.game.clean()
                        snake.calculate_fitness()
                        pop.individuals[i] = snake           
        
            print("Generation :{0:4d}/{1} | [{2}] | best fitness : {3:2.3E} | best score : {4:2d} | lifespan : {5:3d}".format(
                                                                        generation+1, 
                                                                        self.epochs, 
                                                                        "", 
                                                                        pop.fittest.fitness,
                                                                        pop.fittest.score,
                                                                        pop.fittest.lifespan), 
                  end="\n")
            next_pop = []  # For setting next population
            
            # Get best individuals from current pop
            best_from_pop = pop.select_elitism(500)
            next_pop.extend(best_from_pop)
            
            while len(next_pop) < self.num_population:
                p1, p2 = pop.select_roulette_wheel(2)
                # p1, p2 = pop.select_tournament(2, 100)
                mutation_rate = 0.05
            
                # Create offpsring through crossover
                if rd.random() > 0.5:
                    c1_chromosome, c2_chromosome = pop.crossover_simulated_binary(p1, p2, eta=100)
                else:
                    c1_chromosome, c2_chromosome = pop.crossover_single_point(p1, p2)
                    
                snake_child1 = Snake(self.game, chromosomes=c1_chromosome)
                snake_child2 = Snake(self.game, chromosomes=c2_chromosome)    
                
                snake_child1.mutate(mutation_rate)
                snake_child2.mutate(mutation_rate)
                
                next_pop.extend([snake_child1, snake_child2])
                                   
            # Track average fitness
            fitness.append(pop.mean_fitness)
    
            # Set the next generation
            pop.individuals = next_pop
            
        print("\n\nBest individual :\n")
        print(pop.fittest)
        
        plt.yscale('symlog')
        plt.xlabel('Generation')
        plt.ylabel('Fitness')
        plt.plot(range(len(fitness)), fitness, color='steelblue')
        plt.tight_layout()
        plt.show()
                
        return pop



if __name__ == "__main__":
    
    # Global parameters
    BOARD_SIZE = (13, 13)
    CELL_SIZE = 50
    
    # Run
    evolution_game = GameEvolution(BOARD_SIZE, 
                                   CELL_SIZE)
    snakes = [Snake(evolution_game.game) for _ in range(20)]
    evolution_game.evolve()
    # evolution_game.play()


