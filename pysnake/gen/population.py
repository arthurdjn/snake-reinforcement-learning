# -*- coding: utf-8 -*-
# Created on Fri Feb 21 11:01:32 2020
# @author: arthurd


"""
Population set-up for genetic algorithm.
"""

import numpy as np  
import random as rd
from scipy.special import softmax


class Population:
    """
    Abstract class that defines a population.
    A population contains a set of individuals.
    
    Attributes
    ----------
    size : int
    
    
    """
    
    
    def __init__(self, individuals, id = None):
        
        # @NOTE :
        # individuals must be set first
        self.individuals = individuals
        self.__id = id
        self.__size = self.size
        self.__fitness = self.fitness
        self.__mean_fitness = self.mean_fitness
        self.__std_fitness = self.std_fitness
        self.__fittest = self.fittest
        

    # -------------------------------------------------------------------------
    # Methods
        
    def calculate_fitness(self):
        for individual in self.individuals:
            individual.calculate_fitness()
            
            
    def select_elitism(self, num_individuals):
        individuals = sorted(self.individuals, key = lambda individual: individual.fitness, reverse=True)
        return individuals[:num_individuals]
    
    
    def select_roulette_wheel(self, num_individuals):
        
        # Create a wheel based on the fitness of individuals
        # @NOTE : not necessary to use sorted array
        sorted_individuals = sorted(self.individuals, key = lambda individual: individual.fitness, reverse=False)
        sorted_fitness = [individual.fitness for individual in sorted_individuals]
        distribution = softmax(sorted_fitness)
        
        selection = np.random.choice(sorted_individuals, num_individuals, p=distribution)
                    
        return selection
    
    
    def simulated_binary_crossover(self, parent1, parent2, eta):
        
        # Calculate Gamma (Eq. 9.11)
        rand = np.random.random(parent1.chromosome.shape)
        gamma = np.empty(parent1.chromosome.shape)
        gamma[rand <= 0.5] = (2 * rand[rand <= 0.5]) ** (1.0 / (eta + 1))  # First case of equation 9.11
        gamma[rand > 0.5] = (1.0 / (2.0 * (1.0 - rand[rand > 0.5]))) ** (1.0 / (eta + 1))  # Second case
    
        # Calculate Child 1 chromosome (Eq. 9.9)
        chromosome1 = 0.5 * ((1 + gamma)*parent1.chromosome + (1 - gamma)*parent2.chromosome)
        # Calculate Child 2 chromosome (Eq. 9.10)
        chromosome2 = 0.5 * ((1 - gamma)*parent1.chromosome + (1 + gamma)*parent2.chromosome)
    
        return chromosome1, chromosome2
    
    
    def __getitem__(self, index):
        return self.individuals[index]
    
    
    # -------------------------------------------------------------------------
    # Getters and setters

    @property
    def size(self):
        return len(self.individuals)

    @size.setter
    def size(self, value):
        raise AttributeError("attribute 'size' of 'Population' objects is not writable.",
                             "Change attribute 'individuals' instead.")

    # @property
    # def num_genes(self):
    #     return self.individuals[0].chromosome.shape[1]

    # @num_genes.setter
    # def num_genes(self, value):
    #     raise AttributeError("attribute 'num_genes' of 'Population' objects is not writable.",
    #                          "Change attribute 'individuals' instead.")

    @property
    def fitness(self):
        return np.array([individual.fitness for individual in self.individuals])
    
    @fitness.setter
    def fitness(self, value):
        raise AttributeError("attribute 'fitness' of 'Population' objects is not writable.",
                             "Change attribute 'individuals' instead.")

    @property
    def mean_fitness(self):
        return np.mean(self.fitness)

    @mean_fitness.setter
    def mean_fitness(self, value):
        raise AttributeError("attribute 'mean_fitness' of 'Population' objects is not writable.",
                             "Change attribute 'individuals' instead.")

    @property
    def std_fitness(self):
        return np.std(self.fitness)
    
    @std_fitness.setter
    def std_fitness(self, value):
        raise AttributeError("attribute 'std_fitness' of 'Population' objects is not writable.",
                             "Change attribute 'individuals' instead.") 

    @property
    def fittest(self):
        return max(self.individuals, key = lambda individual: individual.fitness)

    @fittest.setter
    def fittest(self, value):
        raise AttributeError("attribute 'fittest' of 'Population' objects is not writable.",
                             "Change attribute 'individuals' instead.")
