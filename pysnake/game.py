# -*- coding: utf-8 -*-
# Created on Sun Feb 16 12:48:18 2020
# @author: arthurd


# Useful packages
import os
import numpy as np
import random as rd
# Test if pygame is installed
try:
    import pygame
except ModuleNotFoundError:
    print("Module PyGame is not installed.\nEither install this package or turn off the 'render' parameter in the config.ini file.")

# PySnake modules
from pysnake.enum import Item, Direction
from pysnake.grid import Cell, Grid
from pysnake.snake import Snake
from pysnake.windraw import WindowGame
from pysnake.io import save_snake
# Neural Network and Genetic Algorithm
from pysnake.gen.population import Population
from pysnake.nn.functional import softmax, relu, tanh, leaky_relu, linear



class Game:
    """
    Game board. This class interracts with the grid, snake(s), apple(s) and all
    elements used in the snake game. It does not depends on pysnake.
    
    Attributes
    ----------
    seed: int
        Fix random numbers.
    grid: pysnake.grid.Grid
        Grid containing cells (apples, snake(s)...).
    shape: tuple(int, int)
        Shape of the grid.
    snakes: list(pysnake.snake.Snake)
        List of all snakes in the game.
    apples: list(pysnake.grid.Cell)
        List of apple cells in the game.
    """
    
    def __init__(self, shape=None, grid=None, seed=None):
        
        assert not (shape is None and grid is None), ('Cannot create a game without specifying at least shape.') 
        
        # Fix random numbers, use for debug mode
        self.seed = seed
        np.random.seed(seed)
        rd.seed(seed)
        
        if grid is None:
            grid = Grid(shape)
            # Add borders to the grid
            grid.add_wall_borders()
        self.grid = grid
        self.shape = grid.shape

        self.snakes = []
        self.apples = []
              
        
    def add_snake(self, snake=None, **kwargs):
        """
        Add a snake to the game.

        Parameters
        ----------
        snake : pysnake.snake.Snake, optional
            Snake to add to the current game. The default is None.
        **kwargs : snake parameters
            Specify to create a snake using these parameters.

        Returns
        -------
        None.
        """
        if snake is None:
            snake = Snake(self, **kwargs)
        else:
            # Update the snake to the game
            snake.game = self
            snake.full_vision.grid = self.grid
            snake.next_direction()
        # Add the snake to the game
        self.snakes.append(snake)
        self.grid.set_cell(*snake.body)
    
    
    def add_apple(self):
        """
        Add a new apple in the game.

        Returns
        -------
        None.
        """
        apple = self.generate_apple()
        self.apples.append(apple)
        # Update the grid
        self.grid.set_cell(apple)
      
        
    def generate_apple(self):
        """
        Generate an apple at an availble cell randomly.

        Returns
        -------
        apple : pysnake.grid.Cell
            Cell containing the new apple.
        """
        height, width = self.shape
        available_coord = []
        
        # Check the available cells
        for i in range(height):
            for j in range(width):
                cell = self.grid[i, j]
                # If the cell is empty, add it to the available cells list
                if cell.is_empty():
                    available_coord.append(cell.coord)
                    
        # Choose a position among all
        coord = rd.choices(available_coord)[0]
        apple = Cell(coord, Item.APPLE)
                
        return apple
        
    
    def clean(self):
        """
        Clean the game from previous state (snakes and apples).

        Returns
        -------
        None.
        """
        # Kill the snakes
        for snake in self.snakes:
            snake.kill()
        self.snakes = []     
        # Delete all apples
        for apple in self.apples:
            self.grid.set_empty(apple.coord)
        self.apples = []
        

    def start(self, snake=None, **kwargs):
        """
        (Re)Start a game

        Parameters
        ----------
        snake : pysnake.snake.Snake, optional
            Snake used to start a new game. The default is None.
        **kwargs : parameters
            Custom parameters to initialize the snake.

        Returns
        -------
        None.
        """
        self.clean()
        self.add_snake(snake, **kwargs)
        self.add_apple()     
        snake.update()




class GameApplication:
    """
    Game application, interacting with the user. This class is used to play 
    and train snakes.
    
    Attributes
    ----------
    
    """
    
    
    def __init__(self, config):

        # Main Game
        # ---------
        self.board_size = eval(config.get('Game', 'board_size'))
        self.seed = eval(config.get('Game', 'seed'))
        self.game = Game(self.board_size, seed = self.seed)
        
        # WindowGame
        # ----------
        self.show = eval(config.get('WindowGame', 'render'))
        # Render the game in pygame
        if self.show:
            # Create a pygame screen
            self.cell_size = eval(config.get('WindowGame', 'cell_size'))
            screen_size = (self.cell_size * (self.board_size[1] * 2), 
                           self.cell_size * (self.board_size[0]))
            self.pygame_win = pygame.display.set_mode(screen_size)
            # Set the fps
            self.clock = pygame.time.Clock() 
            self.fps_play = eval(config.get('WindowGame', 'fps_play'))
            self.fps_train = eval(config.get('WindowGame', 'fps_train'))
            # Set the game bbox
            x0, y0 = (self.board_size[1] * self.cell_size, 0)
            width, height = (self.board_size[1] * self.cell_size, self.board_size[0] * self.cell_size)
            bbox_game = (x0, y0, width, height)
            # Set the network bbox
            x0, y0 = (0, 0)
            width, height = (self.board_size[1] * self.cell_size, self.board_size[0] * self.cell_size)
            bbox_network = (x0, y0, width, height)
            
            self.window_game = WindowGame(self.game, self.pygame_win, 
                                          cell_size = self.cell_size, 
                                          bbox_game = bbox_game,
                                          bbox_network = bbox_network)
            self.show_grid = eval(config.get('WindowGame', 'show_grid'))
            self.show_vision = eval(config.get('WindowGame', 'show_vision'))
        
        # In Game Status
        # ------
        self._pause = True
        self._run = False
        
        # Snakes Inner Params
        # -------------------
        self.snake_params = {
            "length": eval(config.get('Snake', 'length')),
            "vision_type": eval(config.get('Snake', 'vision_type')),
            "vision_mode": eval(config.get('Snake', 'vision_mode')),
            "lifespan_max": eval(config.get('Snake', 'lifespan_max')),
            "hunger_max": eval(config.get('Snake', 'hunger_max')),
            # Neural Network
            "nn_hidden_layers": eval(config.get('NeuralNetwork', 'hidden_layers')),
            # self.activation_hidden = eval(config.get('NeuralNetwork', 'activation_hidden')),
            # self.activation_output = eval(config.get('NeuralNetwork', 'activation_output'))
            }
                            
        # Genetic Algorithm
        # -----------------       
        # Saving
        self.save_best_individuals = eval(config.get('GeneticAlgorithm', 'save_best_individuals'))
        self.save_generations = eval(config.get('GeneticAlgorithm', 'save_generations'))
        self.save_steps = eval(config.get('GeneticAlgorithm', 'save_steps'))
        self.save_dir = eval(config.get('GeneticAlgorithm', 'save_dir'))
        # Training
        self.num_generations = eval(config.get('GeneticAlgorithm', 'num_generations'))
        self.num_parents = eval(config.get('GeneticAlgorithm', 'num_parents'))
        self.num_offspring = eval(config.get('GeneticAlgorithm', 'num_offspring'))
        self.num_population = self.num_parents + self.num_offspring
        self.eta_SBX = eval(config.get('GeneticAlgorithm', 'eta_SBX'))
        self.probability_SBX = eval(config.get('GeneticAlgorithm', 'probability_SBX'))
        self.probability_SPBX = eval(config.get('GeneticAlgorithm', 'probability_SPBX'))
        self.crossover_selection_type = eval(config.get('GeneticAlgorithm', 'crossover_selection_type'))
        self.mutation_rate = eval(config.get('GeneticAlgorithm', 'mutation_rate'))
        # self.mutation_rate_type = str(config.get('GeneticAlgorithm', 'mutation_rate_type'))
        self.gaussian_mu = eval(config.get('GeneticAlgorithm', 'gaussian_mu'))
        self.gaussian_std = eval(config.get('GeneticAlgorithm', 'gaussian_std'))
        

    def _player_controler(self, snake):
        """
        Key listener. Interaction machine - user.

        Parameters
        ----------
        snake : pysnake.snake.Snake
            The snake to interact with.

        Returns
        -------
        snake : pysnake.snake.Snake
            The modified (or new) snake.
        """
        # Quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._run = False
                pygame.quit()
                quit()
        
        # Update the direction
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            snake.direction = Direction.UP
            self._pause = False
        elif keys[pygame.K_RIGHT]:
            snake.direction = Direction.RIGHT
            self._pause = False
        elif keys[pygame.K_DOWN]:
            snake.direction = Direction.DOWN
            self._pause = False
        elif keys[pygame.K_LEFT]:
            snake.direction = Direction.LEFT
            self._pause = False
        
        # Pause the game
        elif keys[pygame.K_SPACE]:
            self._pause = not self._pause
            print(snake.compute_input())
            
       # Restart a game
        elif keys[pygame.K_r]:
            self._pause = True
            self.game.seed = snake.seed
            snake = Snake(self.game, **snake.get_params())
            self.game.start(snake)
        
        # Show the vision
        elif keys[pygame.K_v]:
            self.show_vision = not self.show_vision
        
        # Show the grid
        elif keys[pygame.K_g]:
            self.show_grid = not self.show_grid
                
        # Increasing / Decreasing the fps
        elif keys[pygame.K_KP_PLUS]:
            self.fps_play += 1
            self.fps_train += 1
        elif keys[pygame.K_KP_MINUS]:
            self.fps_play -= 1
            self.fps_train -= 1
            
        return snake
                       

    def play(self, snake=None):      
        """
        Playble snake game.

        Parameters
        ----------
        snake : pysnake.snake.Snake, optional
            Initial snake. The default is None.

        Returns
        -------
        None.
        """
        # Custom environment
        # self.game.grid.set_wall((0, 1), (2, 3), (2, 4))
        
        # Make sure you can play the game
        run_ai = True
        if snake is None:
            snake = Snake(self.game, **self.snake_params) 
            run_ai = False
        else:
            snake.game = self.game
        self.game.start(snake)
        # Init the activation output for the visuals
        snake.next_direction()
            
        # Run the game until the end
        self._run = True
        while self._run:
            
            # Render the game
            if self.show:
                self.window_game.draw(show_grid=self.show_grid, show_vision=self.show_vision)
                self.clock.tick(self.fps_play)
                # Player controler
                snake = self._player_controler(snake)

            # Always move the snake if not paused
            if not self._pause:
                if run_ai:
                    next_direction = snake.next_direction()
                    snake.direction = next_direction
                # Always move the snake
                is_alive = snake.move()
                # Update the network for visuals
                snake.next_direction()  
                
                # Restart
                if not is_alive:
                    print("----------------")
                    print("You died!")
                    print("Score    : {}".format(snake.score))
                    print("Lifespan : {}".format(snake.lifespan))
                    # Restart a game with the same config / seed / params
                    self.game.seed = snake.seed
                    snake = Snake(self.game, **snake.get_params())
                    self.game.start(snake)
                    # Pause the game at first
                    self._pause = True
                    
    
    def train(self, population=None):
        """
        Train a range of snakes and evolve them.

        Parameters
        ----------
        population : pysnake.gen.population.Population, optional
            Initial population to start from. The default is None.

        Returns
        -------
        population : pysnake.gen.population.Population
            Last evolved population.
        fitness : list(float)
            Fitness of all best individuals from the initial population to 
            the last one.
        """
        fitness = []  # For tracking average fitness over generation
        # Always fix the seed for training
        if self.seed is None:
            self.seed = 0
        
        # Create and initialize the population
        if population is None:
            individuals = [Snake(Game(self.board_size, seed=self.seed+i), **self.snake_params) for i in range(self.num_population)]                
            population = Population(individuals)
               
        for generation in range(self.num_generations):
            next_individuals = []  # For setting next population
            
            # Play all snakes in their games environment
            for i in range(self.num_population):                
                chromosomes = population.individuals[i].chromosomes
                snake = Snake(self.game, chromosomes=chromosomes, **self.snake_params)
                self.game.start(snake)
                # Init activation output for visuals
                snake.next_direction()  
                
                # Run the game until the end
                is_alive = True
                self._pause = False
                while is_alive:
                    
                    # Render the game
                    if self.show:
                        self._player_controler(snake)
                        self.window_game.draw(show_grid=self.show_grid, show_vision=self.show_vision)
                        
                        # Ellapsed time between two frames
                        self.clock.tick(self.fps_train)   

                    if not self._pause:
                        snake.direction = snake.next_direction()
                        is_alive = snake.move()
                        
                        if not is_alive:
                            # Update the population wit the final fitness
                            snake.calculate_fitness()
                            population.individuals[i] = snake  
                            self.game.clean()
                            # Update the seed
                            if self.seed is not None:
                                self.seed += 1
                                self.game.seed = self.seed
            
            # Save ?
            if self.save_best_individuals and generation % self.save_steps == 0:
                dirpath = self.save_dir + os.sep + "fittest"
                filename = "snake_" + str(generation) + ".json"
                save_snake(population.fittest, filename, dirpath = dirpath)

            if self.save_generations and generation % self.save_steps == 0:
                dirpath = self.save_dir + os.sep + "generation_" + str(generation)
                for (i, snake) in enumerate(population.individuals):
                    snake.id = i
                    filename ='snake_' + str(i) + '.json'
                    save_snake(snake, filename, dirpath = dirpath)
            
            # Display a log each generations
            print("----------------------")
            print("Generation  : {0:4d}/{1}".format(generation + 1, self.num_generations), end = " | ")
            print("best fitness: {0:2.3E}".format(population.fittest.fitness), end = " | ")
            print("best score  : {0:2d}".format(population.fittest.score), end = " | ")
            print("lifespan    : {0:3d}".format( population.fittest.lifespan), end = " | ")
            
            # Get best individuals from current pop
            best_from_pop = population.select_elitism(self.num_parents)
            next_individuals.extend(best_from_pop)
            
            while len(next_individuals) < self.num_population:
                parent1, parent2 = population.select_roulette_wheel(2)
                # parent1, parent2 = pop.select_tournament(2, 100)
            
                # Create offpsring through crossover
                if rd.random() > self.probability_SBX:
                    chromosomes_child1, chromosomes_child2 = population.crossover_simulated_binary(parent1, parent2, eta=100)
                else:
                    chromosomes_child1, chromosomes_child2 = population.crossover_single_point(parent1, parent2)
                
                # Create the new individuals
                snake_child1 = Snake(Game(self.board_size), chromosomes=chromosomes_child1, **self.snake_params)
                snake_child2 = Snake(Game(self.board_size), chromosomes=chromosomes_child2, **self.snake_params)    
               
                # Mutate their genes
                mutation_rate = self.mutation_rate
                snake_child1.mutate(mutation_rate)
                snake_child2.mutate(mutation_rate)
                
                next_individuals.extend([snake_child1, snake_child2])
                                   
            # Track average fitness
            fitness.append(population.mean_fitness)
    
            # Set the next generation
            population.individuals = next_individuals
             
        print("======================")
        print("Done !")
        print("Best fitness : {}".format(population.fittest.fitness))
        print("Best individual :\n")
        print(population.fittest)
                        
        return population, fitness
    
        
    
    

if __name__ == "__main__":
    
    # Test the game
    import configparser
    # Load the config
    config_file = "../config.ini"
    config = configparser.ConfigParser()
    config.read(config_file)
    snake_game = GameApplication(config)
    snake_game.play()





        
        