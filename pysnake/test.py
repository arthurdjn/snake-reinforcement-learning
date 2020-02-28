# -*- coding: utf-8 -*-
# Created on Fri Feb 28 02:28:58 2020
# @author: arthurd


# -*- coding: utf-8 -*-
# Created on Sun Feb 16 15:25:05 2020
# @author: arthurd



from pysnake.enum import Direction
from pysnake import Game, Snake
from pysnake.ui import WindowGame

from pysnake.gen import Population, Individual, Chromosome

import random as rd

NUM_INDIVIDUALS = 60
NUM_GENERATIONS = 100
BOARD_SIZE = (15, 15)


# -*- coding: utf-8 -*-
# Created on Sun Feb 16 15:25:05 2020
# @author: arthurd



class GameEvolution:
    
    def __init__(self,
                 board_size=(15, 15), cell_size=20,
                 epochs=3000, num_population=1500):
        
        self.board_size = board_size
        self.cell_size = cell_size
        self.game = Game(self.board_size)
        self.num_population = num_population
        self.epochs = epochs


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
                # Run the game until the end
                is_alive = True
                while is_alive:
                    # Update the direction
                    next_direction = snake.next_direction()
                    snake.direction = next_direction
                    is_alive = snake.move()
                    if not is_alive:
                        self.game.restart()
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

        return pop, fitness



if __name__ == "__main__":
    
    # Global parameters
    BOARD_SIZE = (13, 13)
    CELL_SIZE = 50
    
    # Run
    evolution_game = GameEvolution(BOARD_SIZE, 
                                   CELL_SIZE)
    snakes = [Snake(evolution_game.game) for _ in range(20)]
    pop, fitness = evolution_game.evolve()
    # evolution_game.play()
    
    print("\n", fitness)

